/* eslint-env browser, jquery */
$(document).ready(function () {
  var $button = $('#button')
  var $keyword = $('#keyword')
  var $output = $('#output')
  var $pagination = $('#pagination')

  var opts = {
    lines: 11, // The number of lines to draw
    length: 0, // The length of each line
    width: 7, // The line thickness
    radius: 11, // The radius of the inner circle
    scale: 0.75, // Scales overall size of the spinner
    corners: 0, // Corner roundness (0..1)
    top: '30px'
  }
  var spinner = new Spinner(opts)

  // 格式化字符串 format 函数
  String.prototype.format = function (args) {
    var result = this
    if (arguments.length < 1) {
      return result
    }

    var data = arguments // 如果模板参数是数组
    if (arguments.length === 1 && typeof (args) === 'object') {
      // 如果模板参数是对象
      data = args
    }
    for (var key in data) {
      var value = data[key]
      if (undefined !== value) {
        result = result.replace('{' + key + '}', value)
      }
    }
    return result
  }

  function search (pageParam) {
    if (typeof (pageParam) === 'undefined') pageParam = 1 // 默认页面page=1
    if ($keyword[0].value !== '') { // 防止递归调用自己
      $.ajax({
        type: 'GET',
        url: '/ccp/feed_ajax_data/' + $keyword[0].value + '/' + pageParam,
        beforeSend: function () {
          // 显示 spinner
          spinner.spin($output[0])
        },
        complete: function () {
          // 停止 spinner
          spinner.stop()
        },
        success: function (data) {
          $pagination.html('')  // 清除分页条，防止多次添加
          $output.html(data.output)
          var page = $('#page').text()
          var pages = $('#pages').text()

          if (pages === 1 || pages === 0) {  // 如果：只有1页 或者 没有找到，则：隐藏分页
            $pagination.hide()
          } else {
            $pagination.show()  // 隐藏后记得恢复显示
            var $pagiUl = $('<ul class="pagination"></ul>')
            $pagination.append($pagiUl)
            for (var i = 1; i <= pages; i++) {
              var li = new String('<li id="page-{0}"><a href="#">{1}</a></li>').format(i, i)
              $pagiUl.append(li)
            }
            // 添加高亮
            var $active
            $active = $('#page-{0}'.format(page))
            $active.attr('class', 'active')
            $active.children().removeAttr('href')
          }

          $('li:not(.active)>a').click(function () {
            var pageNum = $(this).text()
            search(pageNum)
          })
        }
      })
    }
  }

  $button.click(function () {
    search()
  })

  document.onkeydown = function (e) {
    if (!e) e = window.event
    if ((e.keyCode || e.which) === 13) {
      search()
    }
  }
})  // document.ready
