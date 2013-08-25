GAME =
    home: ->

    create_accout: ->

    game: ->

        gameViewModel = ->
            vm = @

            vm.actions = ko.observableArray([])

            vm.account = ko.observable()
            vm.otherPlayers = ko.observableArray()

            vm.chosenActions = ko.observableArray([])

            vm.secondsRemaining = ko.computed ->
                total = 10
                for action in vm.chosenActions()
                    total -= action.seconds
                return total

            vm.staminaRemaining = ko.computed ->
                if vm.account()
                    total = vm.account().stamina
                    for action in vm.chosenActions()
                        total += action.stamina
                    if total > 10 then total = 10
                    return total
                else
                    return 0


            vm.chooseAction = (data, event) ->
                thisAction = data
                if vm.secondsRemaining() - thisAction.seconds >= 0 and vm.staminaRemaining() + thisAction.stamina >= 0
                    
                    $.ajax({
                        url: '/api/action/' + data.which + '/'
                        method: 'POST'
                        dataType: 'json'
                        success: (response) ->
                            vm.chosenActions.push(_.cloneDeep(thisAction))
                            vm.addPlayerMovementArrows()
                    })

            vm.currentChatMessage = ko.observable('')


            vm.cancelAction = (data, event) ->
                movePosition = vm.chosenActions.indexOf(data)
                $.ajax({
                    url: '/api/cancel/' + movePosition + '/'
                    method: 'POST'
                    dataType: 'json'
                    success: (response) ->
                        vm.chosenActions.splice(movePosition, vm.chosenActions().length)
                        vm.addPlayerMovementArrows()
                })

            vm.currentTime = ko.observable(new Date())
            vm.clockDisplay = ko.computed ->
                # Get the time until the next 2 minute interval
                #seconds = ((vm.currentTime().getMinutes() % 2) * 60) + vm.currentTime().getSeconds()

                #remaining = 120 - seconds
                #
                #if remaining == 120
                #    return '2:00'
                #else
                #    minDisplay = Math.floor(remaining/60)
                #    secDisplay = remaining % 60
                #    if secDisplay < 10
                #        secDisplay = '0' + (secDisplay+'')
                #    return minDisplay + ':' + secDisplay

                seconds = vm.currentTime().getSeconds()
                seconds = 60 - seconds
                if seconds < 10
                    seconds = '0' + (seconds+'')
                return '0:' + seconds

            vm.clockSeconds = ko.computed ->
                # Get the time until the next 2 minute interval
                #seconds = ((vm.currentTime().getMinutes() % 2) * 60) + vm.currentTime().getSeconds()

                #remaining = 120 - seconds
                #
                #if remaining == 120
                #    return '2:00'
                #else
                #    minDisplay = Math.floor(remaining/60)
                #    secDisplay = remaining % 60
                #    if secDisplay < 10
                #        secDisplay = '0' + (secDisplay+'')
                #    return minDisplay + ':' + secDisplay
                return vm.currentTime().getSeconds()


            vm.doneTypingChat = ->
                $.ajax({
                    url: '/api/update-chat/'
                    method: 'POST'
                    dataType: 'json'
                    data: { 'message': vm.currentChatMessage() }
                })

            setInterval((->
                vm.currentTime(new Date())
                $('title').text('Next in: ' + vm.clockDisplay())
            ), 300)
            
            vm.getActionButtonContent = (icon) ->
                return '<span class="glyphicon ' + icon + '"></span> '

            vm.addPlayerMovementArrows = ->
                $('.arrow').removeClass().addClass('arrow')
                curCol = vm.account().col
                curRow = vm.account().row
                prevDir = vm.account().direction
                curDir = vm.account().direction
                for action in vm.chosenActions()
                    if action.which == 'walk'
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
                        $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.arrow').addClass(prevDir + '-' + curDir)
                    else if action.which == 'run'
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
                        $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.arrow').addClass(prevDir + '-' + curDir)
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
                        $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.arrow').addClass(prevDir + '-' + curDir)
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

                            if action.which == 'walk'
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
                                $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.other-arrow').addClass(prevDir + '-' + curDir)
                            else if action.which == 'run'
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
                                $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.other-arrow').addClass(prevDir + '-' + curDir)
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
                                $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.other-arrow').addClass(prevDir + '-' + curDir)
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
                                $('[data-col="' + curCol + '"][data-row="' + curRow + '"]').find('.other-arrow').addClass(prevDir + '-' + curDir)

                    # Add the other player graphic
                    $square = $('[data-col="' + curCol + '"][data-row="' + curRow + '"]')
                    $square.find('.other-player').addClass(otherPlayer.team).addClass(otherPlayer.direction)
                    if otherPlayer.has_flag
                        $square.find('.other-player').addClass('flag')
                    $square.find('.other-player-name').text(otherPlayer.username + ' (' + otherPlayer.flags_gotten + 'f,' + otherPlayer.enemies_tagged + 't)')


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
                                    break
                    vm.currentChatMessage(vm.account().chat_message)
                    vm.addPlayerMovementArrows()
                    vm.addOthersMovementArrows()
            })

            typingTimer = null
            $('.chat-entry').keyup ->
                clearTimeout(typingTimer)
                typingTimer = setTimeout(vm.doneTypingChat, 1000)


            null

        ko.applyBindings(new gameViewModel)


        $('.actions-panel').on 'mouseover mouseout', '.btn', ->
            $(@).toggleClass('btn-success')
            $(@).toggleClass('btn-danger')
            $(@).nextAll('.btn').toggleClass('btn-success')
            $(@).nextAll('.btn').toggleClass('btn-danger')


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


