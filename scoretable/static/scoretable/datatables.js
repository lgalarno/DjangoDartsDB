/////////////////////////////////////////////////////////////
// DataTable
/////////////////////////////////////////////////////////////
$(document).ready( function () {
    $('#games_table').DataTable({
        "dom": 'ltip',
        "searching": false,
        "columnDefs": [
            { "orderable": false,
                "targets": 6 }
            ]
    }
    );
        $('#standing_table').DataTable({
        "dom": 'lt',
        "searching": false,
    }
    );
} );
