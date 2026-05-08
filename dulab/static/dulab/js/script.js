const { createEditor, createToolbar } = window.wangEditor

const ts = document.querySelectorAll('textarea');
ts.forEach((t, i) => {
	t.style.display = 'none';

	var editor_wrapper = document.createElement('div');
	editor_wrapper.id = 'editor-wrapper-' + i;
	editor_wrapper.style.border = '1px solid #ccc';
	editor_wrapper.style.zIndex = '10000';
	var editor_toolbar = document.createElement('div');
	editor_toolbar.id = 'editor-toolbar-' + i;
	editor_toolbar.style.borderBottom = '1px solid #ccc';
	editor_wrapper.append(editor_toolbar);
	var editor_content = document.createElement('div');
	editor_content.id = 'editor-content-' + i;
	editor_content.style.height = '500px';
	editor_wrapper.append(editor_content);

	t.after(editor_wrapper);

	var editor = createEditor({
		selector: '#' + editor_content.id,
		html: t.value,
		config: {
			onChange(editor) {
				t.value = editor.getHtml();
			},
			MENU_CONF: {
				uploadImage: {
					server: '{{ url("dulab:photo-upload") }}',
					fieldName: 'image',
					maxNumberOfFiles: 10,
					allowedFileTypes: ['image/*'],
					headers: {
						'X-CSRFToken': '{{ csrftoken }}',
					}
				}
			}
		},
		mode: 'default'
	});

	var editor_toolbar = createToolbar({
		editor,
		selector: '#' + editor_toolbar.id,
		config: {
			excludeKeys: ['uploadVideo'],
		},
		mode: 'default'
	});
});
