# ckanext-media

`ckanext-media` is a CKAN extension that provides a flexible and centralized system for managing various media files (such as images, documents, and custom file types) using CKAN's core logic. It is designed to be a reusable solution for handling media assets across different parts of a CKAN site.

Main storage path that is used: `ckan.storage_path config` CKAN config + `media` folder.

Check full [documentation](https://datashades.github.io/ckanext-media/) for more information on how to use this extension.

## Features

- Store and manage media files with custom MIME type restrictions.
- Define multiple **media types** (e.g., Image, File, Banner, etc.).
- Use CKAN’s existing upload infrastructure (similar to user or group image uploads).
- Easily reference media using **media IDs** or **media keys** for templates or extensions.
- Centralized control through the Media UI—no need to modify code to update assets like banners or backgrounds.
- Optional fine-grained MIME type restrictions per media type.

## Use Cases

- Upload and manage homepage banners, backgrounds, or other UI graphics without hardcoding them.
- Store shared documents or files that are not tied to a specific dataset or organization.
- Reference uploaded media across templates via a helper functions:

    * `h.get_media_fileurl_by_id("1")`
    * `h.get_media_fileurl_by_key("my_custom_key")`
    * `h.get_media_fileurl_by_filename("FILEMANE")`.

## Installation

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv
```
git clone https://github.com/Datashades/ckanext-media.git
cd ckanext-media
pip install -e .
```
3. Add `media` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

3. Initialize `media` table in the DB.
```
ckan -c CKAN_CONFIG_PATH db upgrade -p media
```

4. Restart CKAN

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
