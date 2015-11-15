        <div class="modal fade" id="myModal" tabindex="-1" role="dialog"
             aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span
                                aria-hidden="true">&times;</span></button>
                        <h4 class="modal-title" id="myModalLabel">Upload to Rosafi Cloud Storage</h4>
                    </div>
                    <div class="modal-body">
                        Select a file to transfer to your Cloud Storage Account

                        <input type="file"
                               id="choose-button" value="Select a file"
                                >

                        <div class="panel-body">

                            <!-- Standar Form -->
                            <h4>Select files from your computer</h4>
                            <form action="" method="post" enctype="multipart/form-data" id="js-upload-form">
                                <div class="form-inline">
                                    <div class="form-group">
                                        <input type="file" name="files[]" id="js-upload-files" multiple>
                                    </div>
                                    <button type="submit" class="btn btn-sm btn-primary" id="js-upload-submit">Upload files</button>
                                </div>
                            </form>

                            <!-- Drop Zone -->
                            <h4>Or drag and drop files below</h4>
                            <div class="upload-drop-zone" id="drop-zone">
                                Just drag and drop files here
                            </div>

                            <!-- Progress Bar -->
                            <div class="progress">
                                <div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 60%;">
                                    <span class="sr-only">60% Complete</span>
                                </div>
                            </div>

                            <!-- Upload Finished -->
                            <div class="js-upload-finished">
                                <h3>Processed files</h3>
                                <div class="list-group">
                                    <a href="#" class="list-group-item list-group-item-success"><span class="badge alert-success pull-right">Success</span>image-01.jpg</a>
                                    <a href="#" class="list-group-item list-group-item-success"><span class="badge alert-success pull-right">Success</span>image-02.jpg</a>
                                </div>
                            </div>
                        </div>






                    </div>
                    <div class="modal-footer">

                        <input type="button" class="btn btn-primary" value="Upload" onclick="startUploading()" >
                        <button type="button" class="btn btn-default" data-dismiss="modal">Cancel
                        </button>

                    </div>
                </div>
            </div>
        </div>
