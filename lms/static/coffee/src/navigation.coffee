class @Navigation
  constructor: ->
    if $('#accordion').length
      # First look for an active section
      active = $('#accordion ul:has(li.active)').index('#accordion ul')
      # if we didn't find one, look for an active chapter
      if active < 0
        active = $('#accordion h3.active').index('#accordion h3')
      # if that didn't work either, default to 0
      if active < 0
        active = 0
      $('#accordion').bind('accordionchange', @log).accordion
        active: active
        header: 'h3'
        autoHeight: false
      $('#open_close_accordion a').click @toggle

      $('#accordion').show()

  log: (event, ui) ->
    log_event 'accordion',
      newheader: ui.newHeader.text()
      oldheader: ui.oldHeader.text()

  toggle: ->
    $('.course-wrapper').toggleClass('closed')
