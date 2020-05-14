$(document).ready( function () {
    $('#games_table').DataTable({
        "dom": 'ltip',
        "searching": false,
        "columnDefs": [
            { "orderable": false,
                "targets": 0 }
            ]
    }
    );
        $('#standing_table').DataTable({
        "dom": 'lt',
        "searching": false,
    }
    );
} );


