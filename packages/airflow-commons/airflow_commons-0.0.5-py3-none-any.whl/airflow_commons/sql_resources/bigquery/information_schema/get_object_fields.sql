SELECT
  REPLACE(field_path, 'object.', '') AS field_path
FROM {project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS
WHERE table_name='{table_name}'
  AND column_name = 'object'
  AND field_path NOT IN ('object',
    'object.type',
    'object.id');
