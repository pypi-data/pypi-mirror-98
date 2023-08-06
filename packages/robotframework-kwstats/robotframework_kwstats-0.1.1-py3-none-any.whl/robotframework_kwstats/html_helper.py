def get_html_content(value):
    html_content = """
    <!DOCTYPE doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
        <link href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css" rel="stylesheet"/>
        <link href="https://cdn.datatables.net/buttons/1.5.2/css/buttons.dataTables.min.css" rel="stylesheet"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
        <!-- Bootstrap core Datatable-->
        <script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js" type="text/javascript"></script>
        <script src="https://cdn.datatables.net/buttons/1.5.2/js/dataTables.buttons.min.js" type="text/javascript"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js" type="text/javascript"></script>
        <script src="https://cdn.datatables.net/buttons/1.5.2/js/buttons.html5.min.js" type="text/javascript"></script>
        <script src="https://cdn.datatables.net/buttons/1.5.2/js/buttons.print.min.js" type="text/javascript"></script>
        <script src="https://cdn.datatables.net/buttons/1.6.1/js/buttons.colVis.min.js" type="text/javascript"></script>
        <style>
            .dt-buttons {
                margin-left: 5px;
            }
        </style>
    </head>
    <body>
        <table style="width: 100%%;">
            <tbody>
                <tr>
                <td>
                    <h2 style="color:Brown;padding-left: 10px;">Keyword Statistics</h2>
                </td>
                </tr>
            </tbody>
        </table>
        <br>
        <table id="example" class="display" style="width:100%%">
            <thead>
                <tr>
                    <th rowspan="2" style="text-align:center">Suite/File</th>
                    <th rowspan="2" style="text-align:center">Kw Name</th>
                    <th rowspan="2" style="text-align:center">Count</th>
                    <th rowspan="2" style="text-align:center">Pass %%</th>
                    <th colspan="4" style="text-align:center">Time(s)</th>
                </tr>
            <tr>
                    <th style="text-align:center">Min</th>
                    <th style="text-align:center">Max</th>
                    <th style="text-align:center">Average</th>
                    <th style="text-align:center">Total</th>
                </tr>
            </thead>
            <tbody>
            %s
            </tbody>
        </table>
        <script>
            $(document).ready(function() {
                $('#example').DataTable({
                    "order": [
                        [2, "desc"]
                    ],
                "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
                dom: 'l<".margin" B>frtip',
                        buttons: [
                            {
                                extend:    'copyHtml5',
                                text:      '<i class="fa fa-files-o"></i>',
                                titleAttr: 'Copy',
                                exportOptions: {
                                columns: ':visible'
                                }
                            },
                            {
                                extend:    'csvHtml5',
                                text:      '<i class="fa fa-file-text-o"></i>',
                                titleAttr: 'CSV',
                                filename: function() {
                                    return 'KwStats';
                                },
                                exportOptions: {
                                    columns: ':visible'
                                }
                            },
                            {
                                extend:    'excelHtml5',
                                text:      '<i class="fa fa-file-excel-o"></i>',
                                titleAttr: 'Excel',
                                    filename: function() {
                                        return 'KwStats';
                                    },
                                exportOptions: {
                                columns: ':visible'
                                }
                            },
                            {
                                extend:    'print',
                                text:      '<i class="fa fa-print"></i>',
                                titleAttr: 'Print',
                                exportOptions: {
                                columns: ':visible',
                                    alignment: 'left',
                                }
                            },
                                {
                                extend:    'colvis',
                                collectionLayout: 'fixed two-column',
                                text:      '<i class="fa fa-low-vision"></i>',
                                titleAttr: 'Hide Column',
                                exportOptions: {
                                    columns: ':visible'
                                },
                                postfixButtons: [ 'colvisRestore' ]
                            },
                        ],
                        columnDefs: [ {
                            visible: false,
                        } ]
                    });
                });
        </script>        
    </body>
    </html>
    """%(str(value))
    return html_content