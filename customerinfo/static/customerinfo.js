/*
 * variables and functions
 */


/* compose template string */
String.prototype.compose = (function () {
    var re = /%%(.+?)%%/g;
    return function (o) {
        return this.replace(re, function (_, k) {
            return typeof o[k] != 'undefined' ? o[k] : '';
        });
    };
}());


function load_table_events() {
    $('.needsReview').on('mouseenter', function() {
        $(this).attr('class', 'activeRow');
    });
    $('.needsReview').on('mouseleave', function() {
        $(this).attr('class', 'needsReview');
    });
    $('.activeRow').on('mouseenter', function() {
        $(this).attr('class', 'activeRow');
    });
    $('.activeRow').on('mouseleave', function() {
        $(this).attr('class', 'needsReview');
    });
}


/* remove all rows except header */
function emptyCustomerList() {
    $('#customer_list table').find("tr:gt(0)").remove();
}


/* dynamically build customer list */
function buildCustomerList(data) {
    /* 
     * variables that predefined in embedded js in template customerlist.html:
     *   row_tmpl
     *   empty_row_tmpl
     */
    var htmls = [];
    var list = $('#customer_list');
    var header = $('#clst_header');
    var customers = data.customers;
    if (customers.length > 0) {
        for (var i=0; i<customers.length; i++) {
            var row = row_tmpl.compose({
                'C_ID': customers[i].id,
                'NAME_IMG': customers[i].img,
                'C_FIRST_NAME': customers[i].first_name,
                'C_LAST_NAME': customers[i].last_name,
                'C_STATE': customers[i].state,
                'C_EMAIL': customers[i].email,
                'C_PHONE': customers[i].phone,
                'C_CREATED': customers[i].created
            });
            htmls.push(row);
        }
    } else {
        htmls.push(empty_row_tmpl.compose({'COLCNT': data.colcnt}));
    }
    header.after(htmls.join('\n'));
    list.show();
    load_table_events();
}


/* handle customer list search/sorting */
function ajax_clst_search() {
    // avoid page reload after ajax call
    event.preventDefault();

    $.ajax({
        type: "POST",
        crossOrigin: true,
        url: "/ajax/clst_search/",
        data: $('#search_form').serialize(),
        beforeSend: function() {
            emptyCustomerList();
            $('#clst_loading').show();
        },
        success: function(rsp_data, status) {
            $('#clst_loading').hide();
            buildCustomerList(rsp_data);
        },
        error: function(xhr, status, error) {
            $('#clst_loading').hide();
            $('#clst_loading span').text(error);
        },
        complete: function(xhr, status) {
            ;
        }
    });
}


/* dynamically build note list */
function buildNoteList(data) {
    /* 
     * variables that predefined in embedded js in template:
     *   login_user_id
     *   row_tmpl
     *   action_btns_tmpl
     *   empty_row_tmpl
     */
    var htmls = [];
    var list = $('#notelist');
    var notes = data.notes;
    if (notes.length > 0) {
        for (var i=0; i<notes.length; i++) {
            var action_btn_html = '';
            if (login_user_id == notes[i].author_id) {
                action_btn_html = action_btns_tmpl;
            }
            var row = row_tmpl.compose({
                'N_ID': notes[i].id,
                'AUTHOR_EMAIL': notes[i].author_email,
                'AUTHOR_IMG': notes[i].author_img,
                'AUTHOR_NAME': notes[i].author_name,
                'N_UPDATED': notes[i].updated,
                'ACTION_BUTTON_HTML': action_btn_html,
                'N_TEXT': notes[i].text
            });
            htmls.push(row);
        }
    } else {
        htmls.push(empty_row_tmpl);
    }
    list.empty();
    list.append(htmls.join('\n'));
    list.show();

    /*
     * set 'click' handler for each action buttion the note list
     */
    $('.action_edit').on('click', function() {
        // get note text
        var text = $(this).parent().parent().parent().find('p').text();
        // get note id
        var nid = $(this).parent().parent().find('.note_id').text().trim();
        $('#form_note_text').val(text);
        $('#form_nid').val(nid);
        $('#form_action_type').val('edit');
        $('#form_action_add').text('Update');
        $('.note_dialog .title').text('Edit Note');
        $('.note_dialog').show('fade 500');
    });
    $('.action_delete').on('click', function() {
        var ans = confirm("Are you sure to delete this note?");
        if (ans) {
            // get note id
            var nid = $(this).parent().parent().find('.note_id').text().trim();
            $('#form_nid').val(nid);
            $('#form_action_type').val('delete');
            ajax_note_action();
        }
    });

    // set mouseover/leave handler to show/hide action buttions
    $('.note_contents').on('mouseover', function() {
        $(this).find('[class*="action_"]').show();
    });
    $('.note_contents').on('mouseleave', function() {
        $(this).find('[class*="action_"]').hide();
    });

    // hide action buttion at beginning
    $('.note_contents [class*="action_"]').hide();
}


/* handle actions on note: add/edit/delete */
function ajax_note_action() {
    // avoid page reload after ajax call
    event.preventDefault();

    $.ajax({
        type: "POST",
        crossOrigin: true,
        url: "/ajax/note_action/",
        data: $('#note_form').serialize(),
        beforeSend: function() {
            $('.note_dialog').hide();
            $('#cmtlst_loading').show();
        },
        success: function(rsp_data, status) {
            $('#cmtlst_loading').hide();
            buildNoteList(rsp_data);
        },
        error: function(xhr, status, error) {
            $('#cmlst_loading').hide();
            $('#cmlst_loading span').text(error);
        },
        complete: function(xhr, status) {
            ;
        }
    });
}


/* for changing state */
function ajax_change_state() {
    // avoid page reload after ajax call
    event.preventDefault();

    $.ajax({
        type: "POST",
        crossOrigin: true,
        url: "/ajax/change_state/",
        data: $('#state_form').serialize(),
        beforeSend: function() {
            $('#chgsta_loading').show();
        },
        success: function(rsp_data, status) {
            $('#chgsta_loading').hide();
        },
        error: function(xhr, status, error) {
            $('#chgsta_loading').hide();
            $('#chgsta_loading span').text(error);
        },
        complete: function(xhr, status) {
            ;
        }
    });
}


$(document).ready(function() {
    if ($('#search_form').length) {
        /* 
         * customerlist.html
         */
        // set 'click' handler for sorting columns in the header
        $('#clst_header [class*="sortby"]').each(function(i, e) {
            $(this).on('click', function() {
                var sort_col = $(this).attr('class').replace('sortby_', '');
                var curr_sort_col = $('#sort_col').val();
                var curr_sort_dir = $('#sort_dir').val();
                if (sort_col == curr_sort_col) {
                    if (curr_sort_dir == '-') {
                        $('#sort_dir').val('');
                    } else {
                        $('#sort_dir').val('-');
                    };
                } else {
                    // set new sort column
                    $('#sort_col').val(sort_col);
                    // reset sort direction
                    $('#sort_dir').val('');
                };
                ajax_clst_search();
            });
        });
    
        // set 'enter' handler for search button
        $('#search_form').on('submit', function() {
            ajax_clst_search();
        });
    
        // set 'click' handler for search button
        $('#search_form button').on('click', function() {
            ajax_clst_search();
        });

        // load the full customer list at beginning
        ajax_clst_search();
    } else if ($('#note_form').length) {
        /* 
         * customer.html
         */
        // set change handler for state dropdown list
        // if state gets changed, show save & cancel buttons
        $('#form_state').on('change', function() {
            $('.state_actions').css('display', 'inline-block');
        });

        // set click handler for state save button
        $('#state_form_save').on('click', function() {
            // hide state save & cancel buttons
            $('.state_actions').css('display', 'none');
            ajax_change_state();
            // update form_saved_state with new value
            $('#form_saved_state').val($('#form_state').val());
        });

        // set click handler for state cancel button
        $('#state_form_cancel').on('click', function() {
            // avoid page reload after ajax call
            event.preventDefault();

            // hide state save & cancel buttons
            $('.state_actions').css('display', 'none');
            // reset the state back to make it unchanged
            $('#form_state').val($('#form_saved_state').val());
        });

        // set click handler for add buttion in note list header
        $('#action_add').on('click', function() {
            $('#form_action_type').val('add');
            $('#form_action_add').text('Add');
            $('#form_note_text').val();
            //$('.note_dialog .title').text('Add Note');
            $('.note_dialog').show('fade 500');
        });

        // color the textarea border when editing
        $('.note_text').find('textarea').on('focus', function() {
            $(this).css('border', '2px solid #7B9CD3');
        });
        $('.note_text').find('textarea').on('blur', function() {
            $(this).css('border', '2px solid #A9A9A9');
        });

        // save the change status of the note text
        $('#form_note_text').on('change', function() {
            $('#form_changed').val('true');
        });

        // set click handler for add/update button in the note dialog
        $('#form_action_add').on('click', function() {
            // check if note text gets changed or not
            if ($('#form_changed').val() == 'true') {
                ajax_note_action();
                // reset the change status
                $('#form_changed').val('false');
            }
        });

        // set click handler for cancel button in the note dialog
        $('#form_action_cancel').on('click', function() {
            // avoid page reload after ajax call
            event.preventDefault();

            $('#form_changed').val('false');
            $('.note_dialog').hide();
        });
        // load all notes of the customer at beginning
        ajax_note_action();
    }
}); // end of document.ready
