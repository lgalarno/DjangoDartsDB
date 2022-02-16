/////////////////////////////////////////////////////////////
// DataTable
/////////////////////////////////////////////////////////////
$(function() {
    $('#games_table').DataTable({
        "dom": 'ltip',
        "searching": false,
        "columnDefs": [
            { "orderable": false,
                "targets": -1 }
            ]
    }
    );
        $('#standing_table').DataTable({
        "dom": 'lt',
        "searching": false,
    }
    );
}
);
