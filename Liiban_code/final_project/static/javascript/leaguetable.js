// this was taken from the Datatables documentation
//this is the standard form of datatable application
 $(document).ready(function() {
   //apply datatables to html table and saving the school in a variable to call for indexing
     var index = $('#table1').DataTable( {
         "columnDefs": [ {
             "searchable": false,
             "orderable": false,
             "targets": 0
         } ],
         //setting the sort order on the rows in descending so highest schools first
         "order": [[ 2, "desc" ], [3, "desc"], [4, "desc"]]
     } );

     //applying the ranking on the datatable from 1- size of list
     index.on( 'order.dt search.dt', function () {
         index.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
             cell.innerHTML = i+1;
         } );
     } ).draw();
 } );
