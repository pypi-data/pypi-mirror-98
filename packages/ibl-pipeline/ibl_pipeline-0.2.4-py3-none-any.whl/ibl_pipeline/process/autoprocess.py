
from ibl_pipeline.process import (
    create_ingest_task,
    delete_update_entries,
    ingest_alyx_raw,
    ingest_membership,
    ingest_shadow,
    ingest_real,
    populate_behavior,
    get_timezone,
    process_histology
)
from ibl_pipeline.ingest import job
from os import path
import datetime
import time
from tqdm import tqdm


def ingest_status(job_key, task, start, end):

    job.TaskStatus.insert1(
        dict(
            **job_key,
            task=task,
            task_start_time=start,
            task_end_time=end,
            task_duration=(end-start).total_seconds()/60.,
        ),
        skip_duplicates=True
    )


def process_new(previous_dump=None, latest_dump=None,
                job_date=datetime.date.today().strftime('%Y-%m-%d'),
                timezone='other'):

    job_key = dict(
        job_date=job_date,
        job_timezone=timezone,
    )

    if previous_dump is None:
        previous_dump = path.join('/', 'data', 'alyxfull.json.last')

    if latest_dump is None:
        latest_dump = path.join('/', 'data', 'alyxfull.json')

    print('Comparing json dumps ...')
    create_ingest_task.compare_json_dumps(previous_dump, latest_dump)

    created_pks, modified_pks, deleted_pks, modified_pks_important = (
        job.Job & job_key).fetch1(
            'created_pks', 'modified_pks', 'deleted_pks', 'modified_pks_important')

    print('Deleting modified entries from alyxraw and shadow tables...')
    start = datetime.datetime.now()

    delete_update_entries.delete_entries_from_alyxraw(
        modified_pks, modified_pks_important)

    ingest_status(job_key, 'Delete alyxraw', start, end=datetime.datetime.now())

    print('Deleting modified entries from membership tables...')
    start = datetime.datetime.now()
    delete_update_entries.delete_entries_from_membership(
        modified_pks_important)
    ingest_status(job_key, 'Delete shadow membership', start,
                  end=datetime.datetime.now())

    print('Ingesting into alyxraw...')
    start = datetime.datetime.now()
    ingest_alyx_raw.insert_to_alyxraw(
        ingest_alyx_raw.get_alyx_entries(
            latest_dump, new_pks=created_pks+modified_pks))
    ingest_status(job_key, 'Ingest alyxraw', start, end=datetime.datetime.now())

    print('Ingesting into shadow tables...')
    start = datetime.datetime.now()
    ingest_shadow.main(modified_pks=modified_pks_important)
    ingest_status(job_key, 'Ingest shadow', start, end=datetime.datetime.now())

    print('Ingesting into shadow membership tables...')
    start = datetime.datetime.now()
    ingest_membership.main(created_pks+modified_pks_important)
    ingest_status(job_key, 'Ingest shadow membership', start,
                  end=datetime.datetime.now())

    print('Ingesting alyx real...')
    start = datetime.datetime.now()
    ingest_real.main()
    ingest_status(job_key, 'Ingest real', start, end=datetime.datetime.now())

    print('Updating fields...')
    start = datetime.datetime.now()
    delete_update_entries.update_entries_from_real_tables(
        modified_pks_important)
    ingest_status(job_key, 'Update fields', start, end=datetime.datetime.now())

    print('Ingesting behavior...')
    start = datetime.datetime.now()
    populate_behavior.main(backtrack_days=30)
    ingest_status(job_key, 'Populate behavior', start,
                  end=datetime.datetime.now())


def process_public():

    from ibl_pipeline import public
    from ibl_pipeline.common import subject, acquisition

    ingest_alyx_raw.insert_to_alyxraw(
        ingest_alyx_raw.get_alyx_entries())

    excluded_tables = [
        'Weighing',
        'WaterType',
        'WaterAdministration',
        'WaterRestriction',
        'ProbeModel',
        'ProbeInsertion',
        'ProbeTrajectory'
    ]

    ingest_shadow.main(excluded_tables=excluded_tables)

    excluded_membership_tables = [
        'WaterRestrictionUser',
        'WaterRestrictionProcedure',
        'SurgeryUser',
        'WaterAdministrationSession',
    ]

    ingest_membership.main(
        excluded_tables=excluded_membership_tables)

    ingest_real.main(
        excluded_tables=excluded_tables+excluded_membership_tables,
        public=True)

    # delete non-releasing tables
    from ibl_pipeline.ingest import QueryBuffer

    table = QueryBuffer(acquisition.Session)
    for key in tqdm(
            (acquisition.Session - public.PublicSession - behavior.TrialSet).fetch('KEY')):
        table.add_to_queque1(key)
        if table.flush_delete(chunksz=100):
            print('Deleted 100 sessions')

    table.flush_delete()
    print('Deleted the rest of the sessions')

    subjs = subject.Subject & acquisition.Session

    for key in tqdm(
            (subject.Subject - public.PublicSubjectUuid - subjs.proj()).fetch('KEY')):
        (subject.Subject & key).delete()

    excluded_behavior_tables = [
        'AmbientSensorData',
        'Settings',
        'SessionDelay'
    ]

    populate_behavior.main(excluded_tables=excluded_behavior_tables)


def process_updates(pks, current_dump='/data/alyxfull.json'):
    '''
    Update the all the fields in givens a set of pks
    :param pks: uuids where an update is needed
    :param current_dump: the latest
    '''
    print('Deleting from alyxraw...')
    delete_update_entries.delete_entries_from_alyxraw(
        modified_pks_important=pks)
    print('Deleting from shadow membership...')
    delete_update_entries.delete_entries_from_membership(pks)

    print('Ingesting alyxraw...')
    ingest_alyx_raw.insert_to_alyxraw(
        ingest_alyx_raw.get_alyx_entries(
            current_dump, new_pks=pks))

    print('Ingesting into shadow tables...')
    ingest_shadow.main(excluded_tables=['DataSet', 'FileRecord'])

    print('Ingesting into shadow membership tables...')
    ingest_membership.main(pks)

    print('Ingesting alyx real...')
    ingest_real.main(excluded_tables=['DataSet', 'FileRecord'])

    print('Updating field...')
    delete_update_entries.update_entries_from_real_tables(pks)


if __name__ == '__main__':

    process_new(previous_dump='/data/alyxfull_20210212_0400.json',
                latest_dump='/data/alyxfull.json',
                job_date='2021-02-15', timezone='European')
