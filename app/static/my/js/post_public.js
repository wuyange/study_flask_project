const { createEditor, createToolbar } = window.wangEditor

const editorConfig = {
    placeholder: '请输入文章内容',
    MENU_CONF:{},
    onChange(editor) {
      const html = editor.getHtml()
      console.log('editor content', html)
      // 也可以同步到 <textarea>
    }
}

// editorConfig.MENU_CONF['uploadImage'] = {
//     server: 'front/upload/image',
//     fieldName: 'your-custom-name',
//     maxNumberOfFiles: 1,
//     base64LimitSize: 5 * 1024 * 1024,
//     allowedFileTypes: [],
// }

const editor = createEditor({
    selector: '#editor-container',
    html: '<p><br></p>',
    config: editorConfig,
    mode: 'default', // or 'simple'
})

const toolbarConfig = {}

const toolbar = createToolbar({
    editor,
    selector: '#toolbar-container',
    config: toolbarConfig,
    mode: 'default', // or 'simple'
})

editor.getConfig().MENU_CONF['uploadImage'] = {
    server: '/front/upload/image',
    fieldName: 'image',
    onSuccess(file, res) {          
        console.log(file, res)
        console.log(`${file.name} 上传成功`, res)
    },
}
