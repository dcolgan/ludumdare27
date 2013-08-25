GAME =
    home: ->

    create_accout: ->

    game: ->

        gameViewModel = ->
            vm = @

            vm.actions = ko.observableArray([])

            vm.account = ko.observable()
            vm.otherPlayers = ko.observableArray()

            vm.secondsRemaining = ko.observable(10)
            vm.chosenActions = ko.observableArray([])


            vm.chooseAction = (data, event) ->
                thisAction = data
                if vm.secondsRemaining() - thisAction.seconds >= 0
                    
                    $.ajax({
                        url: '/api/action/' + data.which + '/'
                        method: 'POST'
                        dataType: 'json'
                        success: (response) ->
                            vm.chosenActions.push(_.cloneDeep(thisAction))
                            vm.secondsRemaining(vm.secondsRemaining()-thisAction.seconds)
                            vm.addPlayerMovementArrows()
                    })


            vm.cancelAction = (data, event) ->
                movePosition = vm.chosenActions.indexOf(data)
                $.ajax({
                    url: '/api/cancel/' + movePosition + '/'
                    method: 'POST'
                    dataType: 'json'
                    success: (response) ->
                        vm.secondsRemaining(vm.secondsRemaining()+data.seconds)
                        vm.chosenActions.remove(data)
                        vm.addPlayerMovementArrows()
                })

            vm.currentTime = ko.observable(new Date())
            vm.clockDisplay = ko.computed ->
                # Get the time until the next 2 minute interval
                seconds = ((vm.currentTime().getMinutes() % 2) * 60) + vm.currentTime().getSeconds()

                remaining = 120 - seconds
                
                if remaining == 120
                    return '2:00'
                else
                    minDisplay = Math.floor(remaining/60)
                    secDisplay = remaining % 60
                    if secDisplay < 10
                        secDisplay = '0' + (secDisplay+'')
                    return minDisplay + ':' + secDisplay

            setInterval((->
                vm.currentTime(new Date())
                $('title').text('Next in: ' + vm.clockDisplay())
            ), 1000)
            
            vm.getActionButtonContent = (icon) ->
                return '<span class="glyphicon ' + icon + '"></span> '

            vm.addPlayerMovementArrows = ->
                $('.arrow').removeClass().addClass('arrow')
                curCol = vm.account().col
                curRow = vm.account().row
                prevDir = vm.account().direction
                curDir = vm.account().direction
                for action in vm.chosenActions()
                    if action.which == 'walk' or action.which == 'run'
                        if curDir == 'north'
                            curRow -= 1
                            prevDir = 'south'
                        if curDir == 'south'
                            curRow += 1
                            prevDir = 'north'
                        if curDir == 'east'
                            curCol += 1
                            prevDir = 'west'
                        if curDir == 'west'
                            curCol -= 1
                            prevDir = 'east'
                    else if action.which == 'north' or action.which == 'south' or action.which == 'east' or action.which == 'west'
                        if curDir == 'north'
                            prevDir = 'south'
                        if curDir == 'south'
                            prevDir = 'north'
                        if curDir == 'east'
                            prevDir = 'west'
                        if curDir == 'west'
                            prevDir = 'east'
                        curDir = action.which
                        
                    console.log(prevDir + '-' + curDir)
                    $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.arrow').addClass(prevDir + '-' + curDir)

            vm.addOthersMovementArrows = ->
                $('.other-arrow').removeClass().addClass('other-arrow')

                for otherPlayer in vm.otherPlayers()
                    curCol = otherPlayer.last_col
                    curRow = otherPlayer.last_row

                    prevDir = otherPlayer.last_direction
                    curDir = otherPlayer.last_direction

                    if otherPlayer.last_actions != ''
                        thisPlayersActions = otherPlayer.last_actions.split(',')

                        for actionName in thisPlayersActions
                            action = null
                            for a in vm.actions()
                                if a.which == actionName
                                    action = a
                                    break

                            if action.which == 'walk' or action.which == 'run'
                                if curDir == 'north'
                                    curRow -= 1
                                    prevDir = 'south'
                                if curDir == 'south'
                                    curRow += 1
                                    prevDir = 'north'
                                if curDir == 'east'
                                    curCol += 1
                                    prevDir = 'west'
                                if curDir == 'west'
                                    curCol -= 1
                                    prevDir = 'east'
                            else if action.which == 'north' or action.which == 'south' or action.which == 'east' or action.which == 'west'
                                if curDir == 'north'
                                    prevDir = 'south'
                                if curDir == 'south'
                                    prevDir = 'north'
                                if curDir == 'east'
                                    prevDir = 'west'
                                if curDir == 'west'
                                    prevDir = 'east'
                                curDir = action.which
                                
                            console.log(prevDir + '-' + curDir)
                            $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.other-arrow').addClass(prevDir + '-' + curDir)

                    # Add the other player graphic
                    $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.other-player').addClass(otherPlayer.team).addClass(otherPlayer.direction)


            $.ajax({
                url: '/api/initial-load/'
                method: 'GET'
                dataType: 'json'
                success: (data) ->
                    for action in data.action_data
                        vm.actions.push(action)

                    vm.account(data.account)
                    for otherPlayer in data.other_players
                        vm.otherPlayers.push(otherPlayer)

                    if data.actions != ''
                        actionNames = data.user_actions.split(',')
                        for actionName in actionNames
                            for action in vm.actions()
                                if action.which == actionName
                                    vm.chosenActions.push(_.cloneDeep(action))
                                    vm.secondsRemaining(vm.secondsRemaining() - action.seconds)
                                    break
                    vm.addPlayerMovementArrows()
                    vm.addOthersMovementArrows()
            })


            null

        ko.applyBindings(new gameViewModel)


        $('.actions-panel').on 'mouseover mouseout', '.btn', ->
            $(@).toggleClass('btn-success')
            $(@).toggleClass('btn-danger')


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


