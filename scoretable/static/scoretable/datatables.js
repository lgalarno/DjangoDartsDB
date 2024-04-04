/////////////////////////////////////////////////////////////
// DataTable
/////////////////////////////////////////////////////////////
$(function() {
    $('#games_table').DataTable({
        searching: false,
        columnDefs: [
            { orderable: false,
                targets: -1 }
            ]
    }
    );
        $('#standing_table').DataTable({
            dom: 'lt',
            searching: false,
/*            order: [[-1, 'des']],*/
    }
    );
}
);
