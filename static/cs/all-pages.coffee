GAME =
    home: ->

    create_accout: ->

    game: ->


        gameViewModel = ->
            vm = @

            vm.actions =
                walk: { name: 'Walk', seconds: 1, stamina: 0 }
                run: { name: 'Run', seconds: 1, stamina: 2 }
                left: { name: 'Turn Left', seconds: 1, stamina: 0 }
                right: { name: 'Turn Right', seconds: 1, stamina: 0 }
                reverse: { name: 'Turn Around', seconds: 1, stamina: 0 }

            vm.secondsRemaining = ko.observable(10)
            vm.chosenActions = ko.observableArray([])

            vm.chooseAction = (data, event) ->
                thisAction = vm.actions[$(event.target).data('action')]
                if vm.secondsRemaining() - thisAction.seconds >= 0
                    vm.secondsRemaining(vm.secondsRemaining()-thisAction.seconds)
                    vm.chosenActions.push(thisAction)

            vm.cancelAction = (data, event) ->
                debugger
                

            null

        ko.applyBindings(new gameViewModel)



            updateSecondsRemainingDisplay: ->
                $('#seconds-left').text(@secondsRemaining)

            chooseAction: (which) ->
                $newActionButton = $(actionButtonTemplate)
                $newActionButton.text($(@).data('action'))


                $newAction.text()
                $newAction.click ->
                    $(@).remove()
                $newAction.hover (->
                    $(@).removeClass('btn-success')
                    $(@).addClass('btn-danger')
                ), (->
                    $(@).addClass('btn-success')
                    $(@).removeClass('btn-danger')
                )
                $('.actions-panel').append($newAction)


$ ->
    # Make it so that the csrf token works
    $.ajaxSetup({
        crossDomain: false
        beforeSend: (xhr, settings) ->
            # these HTTP methods do not require CSRF protection
            if not /^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))
    })

    cl = $('body').attr('class')
    if cl then GAME[cl]()


