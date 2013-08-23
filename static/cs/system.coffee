class System
    constructor: ->
        window.TB = @
        $.getJSON '/api/initial-load/', (data, status) =>
            if status == 'success'
                _.extend(@, data.board_consts)
                # Initialize game here

        $(document).keydown (event) =>
            switch event.which
                # 1, 2, 3 keys
                when 49 then null
                when 50 then null
                when 51 then null

        $('.btn-action').click (event) =>
            null


new System()
