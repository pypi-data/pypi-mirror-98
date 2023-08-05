'''

ibl.ingest

This package contains 'shadowed' copies of main tables for external data load
most classes here will be defined using
<downstream_module>.RealClass.definition;

Only if some merging/disambiguation will definitions be augmented/modified
locally in some way with additional attributes and/or tables to facillitate the
difference. These differences should still result in tables compatbile with
data copying via insert from select (e.g: Foo.insert(Bar.fetch()))

NOTE:

Since downstream modules involve cross-module definitions, those modules should
be imported as 'ds_module' in order to prevent the possibility of accidental
linkages to downstream tables in the upstream schema.

For example, in the scenario:

  - foo.py defines Foo
  - bar.py defines Bar referencing foo.Foo

  - ingest.bar imports .. foo (for some other reason than foo.Foo)
  - ingest.bar imports .. bar (to get foo.Foo schema string)
  - ingest.bar.Bar.definition = bar.Bar.definition

Setting ingest.bar.Bar.definition = bar.Bar.definition creates an accidental
link to downstream foo.Foo table because 'bar' points to the downstream
module. If foo/bar had been imported as ds_foo/ds_bar instead, the table
definition syntax would not properly resolve any 'foo' in the scope of
ingest.bar and the definition would fail, also failing to create the bad link.



In this scheme, the 'correct' implementation would instead be:

  - foo.py defines Foo
  - bar.py defines Bar referencing foo.Foo

  - ingest.bar imports .. foo as ds_foo (for some other reason than foo.Foo)
  - ingest.bar imports .. bar as ds_bar (to get foo.Foo schema string)
  - ingest.bar imports . foo (to get ingest.foo.Foo)
  - ingest.bar.Bar.definition = bar.Bar.definition

Now, ingest.bar.Bar is able to use bar.Bar.definition, but the definition
of ingest.bar.Bar is resolved within the scope of ingest.bar as pointing to
ingest.foo.Foo, creating the proper link to the ingest related table.

While this should not happen in the current architecture, following the pattern
outlined here should prevent it in general and so is a good 'safe practice' to
use for the ingest modules.
'''
import logging
import datajoint as dj
from tqdm import tqdm
from . import alyxraw
import os

if os.environ.get('MODE') == 'test':
    dj.config['database.prefix'] = 'test_'

log = logging.getLogger(__name__)


def get_raw_field(key, field, multiple_entries=False, model=None):
    if model:
        query = alyxraw.AlyxRaw.Field & \
            (alyxraw.AlyxRaw & 'model="{}"'.format(model)) & \
            key & 'fname="{}"'.format(field)
    else:
        query = alyxraw.AlyxRaw.Field & key & 'fname="{}"'.format(field)

    return query.fetch1('fvalue') \
        if not multiple_entries and len(query) else query.fetch('fvalue')


class QueryBuffer(object):
    '''
    QueryBuffer: a utility class to help managed chunked inserts
    Currently requires records do not have prerequisites.
    '''
    def __init__(self, rel):
        self._rel = rel
        self._queue = []
        self._delete_queue = []
        self.fetched_results = []

    def add_to_queue1(self, r):
        self._queue.append(r)

    def add_to_queue(self, recs):
        self._queue += recs

    def flush_insert(self, replace=False, skip_duplicates=False,
              ignore_extra_fields=False, allow_direct_insert=False, chunksz=1):
        '''
        flush the buffer
        XXX: ignore_extra_fields na, requires .insert() support
        '''
        kwargs = dict(skip_duplicates=skip_duplicates,
                      ignore_extra_fields=ignore_extra_fields)
        if allow_direct_insert:
            kwargs.update(allow_direct_insert=True)

        qlen = len(self._queue)
        if qlen > 0 and qlen % chunksz == 0:
            try:
                self._rel.insert(
                    self._queue, **kwargs)
            except Exception as e:
                print('error in flush: {}, trying ingestion one by one'.format(e))
                for t in self._queue:
                    try:
                        self._rel.insert1(t, **kwargs)
                    except Exception as e:
                        print('error in flush: {}'.format(e))
            self._queue.clear()
            return qlen
        else:
            return 0

    def flush_delete(self, chunksz=1, quick=True):
        '''
        flush the delete
        '''

        qlen = len(self._queue)
        if qlen > 0 and qlen % chunksz == 0:
            try:
                if quick:
                    (self._rel & self._queue).delete_quick()
                else:
                    (self._rel & self._queue).delete()
            except Exception as e:
                print('error in flush delete: {}, trying deletion one by one'.format(e))
                for t in self._queue:
                    try:
                        if quick:
                            (self._rel & t).delete_quick()
                        else:
                            (self._rel & t).delete()
                    except Exception as e:
                        print('error in flush delete: {}'.format(e))
            self._queue.clear()
            return qlen
        else:
            return 0

    def flush_fetch(self, field, chunksz=1):
        '''
        flush the fetch
        '''
        qlen = len(self._queue)
        if qlen > 0 and qlen % chunksz == 0:
            try:
                self.fetched_results += (self._rel & self._queue).fetch(field)
            except Exception as e:
                print('error in flush fetch: {}, trying fetch one by one'.format(e))
                for t in self._queue:
                    try:
                        self.fetched_results.append((self._rel & self.__queue).fetch1(field))
                    except Exception as e:
                        print('error in flush fetch: {}'.format(e))
            self._queue.clear()
            return qlen
        else:
            return 0


def populate_batch(t, chunksz=1000, verbose=True):

    keys = (t.key_source - t.proj()).fetch('KEY')
    table = QueryBuffer(t)
    for key in tqdm(keys, position=0):
        entry = t.create_entry(key)
        if entry:
            table.add_to_queue1(entry)

        if table.flush_insert(
                skip_duplicates=True,
                allow_direct_insert=True, chunksz=chunksz) and verbose:
            print(f'Inserted {chunksz} {t.__name__} tuples.')

    if table.flush_insert(skip_duplicates=True, allow_direct_insert=True) and verbose:
        print(f'Inserted all remaining {t.__name__} tuples.')
