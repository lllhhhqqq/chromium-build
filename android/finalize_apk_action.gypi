# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This file is meant to be included into an action to provide an action that
# signs and zipaligns an APK.
#
# To use this, create a gyp action with the following form:
#  {
#    'action_name': 'some descriptive action name',
#    'variables': {
#      'input_apk_path': 'relative/path/to/input.apk',
#      'output_apk_path': 'relative/path/to/output.apk',
#    },
#    'includes': [ '../../build/android/finalize_apk.gypi' ],
#  },
#

{
  'message': 'Signing/aligning <(_target_name) APK: <(input_apk_path)',
  'variables': {
    'keystore_path%': '<(DEPTH)/chromium/build/android/ant/chromium-debug.keystore',
    'keystore_name%': 'chromiumdebugkey',
    'keystore_password%': 'chromium',
    'conditions': [
        # Webview doesn't use zipalign or rezip_apk_jar.
        ['android_webview_build==0', {
          'zipalign_path%': ['<!@(find <(android_sdk_root) -name zipalign)'],
          'rezip_apk_jar_path%': '<(PRODUCT_DIR)/lib.java/rezip_apk.jar'
        }, {
          'zipalign_path%': "",
          'rezip_apk_jar_path%': "",
        }],
    ],
  },
  'inputs': [
    '<(DEPTH)/chromium/build/android/gyp/util/build_utils.py',
    '<(DEPTH)/chromium/build/android/gyp/finalize_apk.py',
    '<(keystore_path)',
    '<(input_apk_path)',
  ],
  'outputs': [
    '<(output_apk_path)',
  ],
  'action': [
    'python', '<(DEPTH)/chromium/build/android/gyp/finalize_apk.py',
    '--zipalign-path=<(zipalign_path)',
    '--unsigned-apk-path=<(input_apk_path)',
    '--final-apk-path=<(output_apk_path)',
    '--key-path=<(keystore_path)',
    '--key-name=<(keystore_name)',
    '--key-passwd=<(keystore_password)',
    '--load-library-from-zip-file=<(load_library_from_zip_file)',
    '--rezip-apk-jar-path=<(rezip_apk_jar_path)',
  ],
}
