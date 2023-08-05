'''
This script inserts membership tuples into the membership shadow tables, \
which cannot be inserted with auto-population.
'''

import datajoint as dj
import json
import uuid
from tqdm import tqdm
from ibl_pipeline.ingest import alyxraw, reference, subject, action, acquisition, data, QueryBuffer
from ibl_pipeline.ingest import get_raw_field as grf
from ibl_pipeline.utils import is_valid_uuid


membership_tables = [
    {'dj_current_table': reference.ProjectLabMember,
     'alyx_parent_model': 'subjects.project',
     'alyx_field': 'users',
     'dj_parent_table': reference.Project,
     'dj_other_table': reference.LabMember,
     'dj_parent_fields': 'project_name',
     'dj_other_field': 'user_name',
     'dj_parent_uuid_name': 'project_uuid',
     'dj_other_uuid_name': 'user_uuid'},
    {'dj_current_table': subject.AlleleSequence,
     'alyx_parent_model': 'subjects.allele',
     'alyx_field': 'sequences',
     'dj_parent_table': subject.Allele,
     'dj_other_table': subject.Sequence,
     'dj_parent_fields': 'allele_name',
     'dj_other_field': 'sequence_name',
     'dj_parent_uuid_name': 'allele_uuid',
     'dj_other_uuid_name': 'sequence_uuid'},
    {'dj_current_table': subject.LineAllele,
     'alyx_parent_model': 'subjects.line',
     'alyx_field': 'alleles',
     'dj_parent_table': subject.Line,
     'dj_other_table': subject.Allele,
     'dj_parent_fields': 'line_name',
     'dj_other_field': 'allele_name',
     'dj_parent_uuid_name': 'line_uuid',
     'dj_other_uuid_name': 'allele_uuid'},
    {'dj_current_table': action.WaterRestrictionUser,
     'alyx_parent_model': 'actions.waterrestriction',
     'alyx_field': 'users',
     'dj_parent_table': action.WaterRestriction,
     'dj_other_table': reference.LabMember,
     'dj_parent_fields': ['subject_uuid', 'restriction_start_time'],
     'dj_other_field': 'user_name',
     'dj_parent_uuid_name': 'restriction_uuid',
     'dj_other_uuid_name': 'user_uuid'},
    {'dj_current_table': action.WaterRestrictionProcedure,
     'alyx_parent_model': 'actions.waterrestriction',
     'alyx_field': 'procedures',
     'dj_parent_table': action.WaterRestriction,
     'dj_other_table': action.ProcedureType,
     'dj_parent_fields': ['subject_uuid', 'restriction_start_time'],
     'dj_other_field': 'procedure_type_name',
     'dj_parent_uuid_name': 'restriction_uuid',
     'dj_other_uuid_name': 'procedure_type_uuid'},
    {'dj_current_table': action.SurgeryUser,
     'alyx_parent_model': 'actions.surgery',
     'alyx_field': 'users',
     'dj_parent_table': action.Surgery,
     'dj_other_table': reference.LabMember,
     'dj_parent_fields': ['subject_uuid', 'surgery_start_time'],
     'dj_other_field': 'user_name',
     'dj_parent_uuid_name': 'surgery_uuid',
     'dj_other_uuid_name': 'user_uuid'},
    {'dj_current_table': action.SurgeryProcedure,
     'alyx_parent_model': 'actions.surgery',
     'alyx_field': 'procedures',
     'dj_parent_table': action.Surgery,
     'dj_other_table': action.ProcedureType,
     'dj_parent_fields': ['subject_uuid', 'surgery_start_time'],
     'dj_other_field': 'procedure_type_name',
     'dj_parent_uuid_name': 'surgery_uuid',
     'dj_other_uuid_name': 'procedure_type_uuid'},
    {'dj_current_table': action.OtherActionUser,
     'alyx_parent_model': 'actions.otheractions',
     'alyx_field': 'users',
     'dj_parent_table': action.OtherAction,
     'dj_other_table': reference.LabMember,
     'dj_parent_fields': ['subject_uuid', 'other_action_start_time'],
     'dj_other_field': 'user_name',
     'dj_parent_uuid_name': 'other_action_uuid',
     'dj_other_uuid_name': 'user_uuid'},
    {'dj_current_table': action.OtherActionProcedure,
     'alyx_parent_model': 'actions.otheractions',
     'alyx_field': 'procedures',
     'dj_parent_table': action.OtherAction,
     'dj_other_table': action.ProcedureType,
     'dj_parent_fields': ['subject_uuid', 'other_action_start_time'],
     'dj_other_field': 'procedure_type_name',
     'dj_parent_uuid_name': 'other_action_uuid',
     'dj_other_uuid_name': 'procedure_type_uuid'},
    {'dj_current_table': acquisition.ChildSession,
     'alyx_parent_model': 'actions.session',
     'alyx_field': 'parent_session',
     'dj_parent_table': acquisition.Session,
     'dj_other_table': acquisition.Session,
     'dj_parent_fields': ['subject_uuid', 'session_start_time'],
     'dj_other_field': 'session_start_time',
     'dj_parent_uuid_name': 'session_uuid',
     'dj_other_uuid_name': 'session_uuid',
     'renamed_other_field_name': 'parent_session_start_time'},
    {'dj_current_table': acquisition.SessionUser,
     'alyx_parent_model': 'actions.session',
     'alyx_field': 'users',
     'dj_parent_table': acquisition.Session,
     'dj_other_table': reference.LabMember,
     'dj_parent_fields': ['subject_uuid', 'session_start_time'],
     'dj_other_field': 'user_name',
     'dj_parent_uuid_name': 'session_uuid',
     'dj_other_uuid_name': 'user_uuid'},
    {'dj_current_table': acquisition.SessionProcedure,
     'alyx_parent_model': 'actions.session',
     'alyx_field': 'procedures',
     'dj_parent_table': acquisition.Session,
     'dj_other_table': action.ProcedureType,
     'dj_parent_fields': ['subject_uuid', 'session_start_time'],
     'dj_other_field': 'procedure_type_name',
     'dj_parent_uuid_name': 'session_uuid',
     'dj_other_uuid_name': 'procedure_type_uuid'},
    {'dj_current_table': acquisition.SessionProject,
     'alyx_parent_model': 'actions.session',
     'alyx_field': 'project',
     'dj_parent_table': acquisition.Session,
     'dj_other_table': reference.Project,
     'dj_parent_fields': ['subject_uuid', 'session_start_time'],
     'dj_other_field': 'project_name',
     'dj_parent_uuid_name': 'session_uuid',
     'dj_other_uuid_name': 'project_uuid',
     'renamed_other_field_name': 'session_project'},
    {'dj_current_table': acquisition.WaterAdministrationSession,
     'alyx_parent_model': 'actions.wateradministration',
     'alyx_field': 'session',
     'dj_parent_table': action.WaterAdministration,
     'dj_other_table': acquisition.Session,
     'dj_parent_fields': ['subject_uuid', 'administration_time'],
     'dj_other_field': 'session_start_time',
     'dj_parent_uuid_name': 'wateradmin_uuid',
     'dj_other_uuid_name': 'session_uuid'},
    {'dj_current_table': data.ProjectRepository,
     'alyx_parent_model': 'subjects.project',
     'alyx_field': 'repositories',
     'dj_parent_table': reference.Project,
     'dj_other_table': data.DataRepository,
     'dj_parent_fields': 'project_name',
     'dj_other_field': 'session_start_time',
     'dj_parent_uuid_name': 'project_uuid',
     'dj_other_uuid_name': 'repo_uuid'},
]


def main(new_pks=None, excluded_tables=[]):
    for tab_args in membership_tables:
        table_name = tab_args['dj_current_table'].__name__
        if table_name in excluded_tables:
            continue
        print(f'Ingesting table {table_name}...')
        ingest_membership_table(**tab_args, new_pks=new_pks)


def ingest_membership_table(dj_current_table,
                            alyx_parent_model,
                            alyx_field,
                            dj_parent_table, dj_other_table,
                            dj_parent_fields, dj_other_field,
                            dj_parent_uuid_name, dj_other_uuid_name,
                            renamed_other_field_name=None,
                            new_pks=None):
    '''
    Ingest shadow membership table.
    This function works for the pattern that an alyx parent model contain one or multiple entries of one field
    that have the information in the membership table.


    Arguments:  dj_current_table : datajoint table object, current membership table to ingest
                alyx_parent_model: string, model name inside alyx that contains information of the current table.
                alyx_field       : field of alyx that contains information of current table
                dj_parent_table  : datajoint parent table, corresponding to alyx parent model
                dj_other_table   : datajoint other table to fetch the field from
                dj_parent_fields : string or list of strings, field names to be fetched from the parent table
                dj_other_field   : string, the field table to be fetched from the other table
                dj_parent_uuid_name: string, uuid id name of the parent table
                dj_other_uuid_name: string, uuid id name of the other table
                renamed_other_field_name: string the other field name sometimes renamed in the real table,
                                        the default is None if the field is not renamed
                new_pks          : list of strings of valid uuids, this is the new entries to process, the
                                default is None if all entries are inserted.
    '''
    if new_pks:
        restr = [{'uuid': pk} for pk in new_pks if is_valid_uuid(pk)]
    else:
        restr = {}

    if len(restr) > 1000:
        print('More than 1000 entries to insert, using buffer...')
        buffer = QueryBuffer(alyxraw.AlyxRaw & {'model': alyx_parent_model})
        for r in tqdm(restr):
            buffer.add_to_queue1(r)
            buffer.flush_fetch('KEY', chunksz=200)
        buffer.flush_fetch('KEY')
        alyxraw_to_insert = buffer.fetched_results

    else:
        alyxraw_to_insert = (alyxraw.AlyxRaw & restr &
                             {'model': alyx_parent_model}).fetch('KEY')

    if not alyxraw_to_insert:
        return

    alyx_field_entries = alyxraw.AlyxRaw.Field & alyxraw_to_insert & \
        {'fname': alyx_field} & 'fvalue!="None"'

    keys = (alyxraw.AlyxRaw & alyx_field_entries).proj(**{dj_parent_uuid_name: 'uuid'})

    if type(dj_parent_fields) == str:
        dj_parent_fields = [dj_parent_fields]

    for key in keys:

        if not dj_parent_table & key:
            print(f'The entry {key} is not parent table {dj_parent_table.__name__}')
            continue

        entry_base = (dj_parent_table & key).fetch(*dj_parent_fields, as_dict=True)[0]

        key['uuid'] = key[dj_parent_uuid_name]
        uuids = grf(key, alyx_field, multiple_entries=True,
                    model=alyx_parent_model)
        if len(uuids):
            for uuid in uuids:
                if uuid == 'None':
                    continue
                else:
                    if not dj_other_table & {dj_other_uuid_name: uuid}:
                        print(f'The uuid {uuid} is not datajoint table {dj_other_table.__name__}')
                        continue
                    entry = entry_base.copy()
                    field_value = (dj_other_table & {dj_other_uuid_name: uuid}).fetch1(dj_other_field)
                    if renamed_other_field_name:
                        entry[renamed_other_field_name] = field_value
                    else:
                        entry[dj_other_field] = field_value

                    dj_current_table.insert1(entry, skip_duplicates=True)


if __name__ == '__main__':

    main()
