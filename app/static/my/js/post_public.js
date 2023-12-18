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

$(function (){
  // 提交按钮单击事件
  $("#add_post").click(function (event) {
      var title = $("input[name='title']").val();
      var board_id = $("select[name='board_id']").val();
      var content = editor.getText();
      $.ajax({
          type: 'POST',
          url: '/front/add_post',
          data: {title,board_id,content},
          success: function(response) {
              location.assign("/front/index");
          },
          error: function(error) {
                   alert(error.responseText);//错误信息
             }
        });
  });
});
