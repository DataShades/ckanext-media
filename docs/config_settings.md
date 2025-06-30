**`ckan.upload.media.mimetypes`** - This configuration is required by the CKAN Core uploader to specify the list of global allowed mimetypes for uploaded files. Here is the current list of the default global mimetypes:
```
image/png image/gif image/jpeg text/csv application/pdf application/vnd.ms-excel application/vnd.openxmlformats-officedocument.spreadsheetml.sheet application/msword application/vnd.openxmlformats-officedocument.wordprocessingml.document application/zip application/json text/plain
```

**`ckanext.media.image.allowed_mimetypes`** - List of allowed Mimetypes for Image Media type. Default:
```
image/png image/gif image/jpeg
```

**`ckanext.media.image.max_filesize`** - Maximum filesize allowed for uploading Image. By default is set to `3` (in MB).


**`ckanext.media.file.allowed_mimetypes`** - List of allowed Mimetypes for Image File type. Default:
```
text/csv application/pdf application/vnd.ms-excel application/vnd.openxmlformats-officedocument.spreadsheetml.sheet application/msword application/vnd.openxmlformats-officedocument.wordprocessingml.document application/zip application/json text/plain
```

**`ckanext.media.file.max_filesize`** - Maximum filesize allowed for uploading File. By default is set to `3` (in MB).
