var nb_tags = 0;
var nb_faces = 0;
var tags = new Array();
var faces = new Array();
var current_face = -1;
var current_tag = -1;
var isFace = false;
var current_title = '';
$(document).ready(function() {  

                var fill_tags_tab =function(){
                    var res = $(".tagged");
                    for(var i=0; i<res.length; i++){
                        var tag = $(res[i]);
                        var pos_x = tag.css('left');
                        pos_x = pos_x.substr(0,pos_x.length-2);
                        var pos_y = tag.css('top');
                        pos_y = pos_y.substr(0,pos_y.length-2);
                        var pos_width = tag.css('width');
                        pos_width = pos_width.substr(0,pos_width.length-2);
                        var pos_height = tag.css('height');
                        pos_height = pos_height.substr(0,pos_height.length-2);
                        var t = $(res[i]).find(".tagged_title").text().replace(/(\r\n|\n|\r|\s)/gm," ");
                        var tag_type = $(res[i]).find(".type").text()
                        tags['tag'+i] = {title:t, x:pos_x, y:pos_y, w:pos_width, h:pos_height, type:tag_type};
                    }
                }

                nb_tags = $(this).find(".tagged").length;
                current_tag = nb_tags;
                if(nb_tags > 0){
                    fill_tags_tab();
                }

                var fill_faces_tab =function(){
                    var res = $(".tagged2");
                    for(var i=0; i<res.length; i++){
                        var tag = $(res[i]);
                        var pos_x = tag.css('left');
                        pos_x = pos_x.substr(0,pos_x.length-2);
                        var pos_y = tag.css('top');
                        pos_y = pos_y.substr(0,pos_y.length-2);
                        var pos_width = tag.css('width');
                        pos_width = pos_width.substr(0,pos_width.length-2);
                        var pos_height = tag.css('height');
                        pos_height = pos_height.substr(0,pos_height.length-2);
                        var t = $(res[i]).find(".tagged_title").text().replace(/(\r\n|\n|\r|\s)/gm," ");
                        faces['tag'+i] = {title:t, x:pos_x, y:pos_y, w:pos_width, h:pos_height, type:"face"};
                    }
                }

                nb_faces = $(this).find(".tagged2").length;
                current_face = nb_faces;
                if(nb_faces > 0){
                    fill_faces_tab();
                    console.log(faces);
                }

                $("#imageMap").click(function(e){


                    var image_left = $(this).offset().left;
                    var click_left = e.pageX;
                    var left_distance = click_left - image_left;

                    var image_top = $(this).offset().top;
                    var click_top = e.pageY;
                    var top_distance = click_top - image_top;

                    var mapper_width = $('#mapper').width();
                    var imagemap_width = $('#imageMap').width();

                    var mapper_height = $('#mapper').height();
                    var imagemap_height = $('#imageMap').height();

                    if((top_distance + mapper_height > imagemap_height) && (left_distance + mapper_width > imagemap_width)){
                        $('#mapper').css("left", (click_left - mapper_width - image_left  ))
                        .css("top",(click_top - mapper_height - image_top  ))
                        .css("width","100px")
                        .css("height","100px")
                        .show();
                    }
                    else if(left_distance + mapper_width > imagemap_width){


                        $('#mapper').css("left", (click_left - mapper_width - image_left  ))
                        .css("top",top_distance)
                        .css("width","100px")
                        .css("height","100px")
                        .show();
			
                    }
                    else if(top_distance + mapper_height > imagemap_height){
                        $('#mapper').css("left", left_distance)
                        .css("top",(click_top - mapper_height - image_top  ))
                        .css("width","100px")
                        .css("height","100px")
                        .show();
                    }
                    else{


                        $('#mapper').css("left",left_distance)
                        .css("top",top_distance)
                        .css("width","100px")
                        .css("height","100px")
                        .show();
                    }


                    $("#mapper").resizable({ containment: "parent" });
                    $("#mapper").draggable({ containment: "parent" });
                    
                });


            });

            var hideBox = function(){
                $("#mapper").hide();
            }


            $(".tagged").live("mouseover",function(){
                if($(this).find(".delete").length == 0){
                    $(this).find(".tagged_box").css("display","block");
                    $(this).css("border","2px solid #EEE");

                    $(this).find(".tagged_title").css("display","block");
                }
			

            });

            $(".tagged").live("mouseout",function(){
                if($(this).find(".delete").length == 0){
                    $(this).find(".tagged_box").css("display","none");
                    $(this).css("border","none");
                    $(this).find(".tagged_title").css("display","none");
                }
			

            });

            $(".tagged2").live("mouseover",function(){
                if($(this).find(".delete").length == 0){
                    $(this).find(".tagged_box").css("display","block");
                    $(this).css("border","2px solid #EEE");

                    $(this).find(".tagged_title").css("display","block");
                }
            

            });

            $(".tagged2").live("mouseout",function(){
                if($(this).find(".delete").length == 0){
                    $(this).find(".tagged_box").css("display","none");
                    $(this).css("border","none");
                    $(this).find(".tagged_title").css("display","none");
                }
            

            });

            $(".tagged").live("click",function(){
                console.log($(this).parent().attr('id'));
                $(this).find(".tagged_box").html("<img src='"+del+"' class='delete' value='Delete' onclick='deleteTag(this)' />\n\
        <img src='"+save+"' class='save' onclick='editTag2(this);' value='Save' />");
                

                var img_scope_top = $("#imageMap").offset().top + $("#imageMap").height() - $(this).find(".tagged_box").height();
                var img_scope_left = $("#imageMap").offset().left + $("#imageMap").width() - $(this).find(".tagged_box").width();

                $(this).draggable({ containment:[$("#imageMap").offset().left,$("#imageMap").offset().top,img_scope_left,img_scope_top]  });

            });

            $(".tagged2").live("click",function(){
                console.log($(this).parent().attr('id'));
                isFace = true;
                 
                $(this).find(".tagged_box").html("<img src='"+del+"' class='delete' value='Delete' onclick='deleteFace(this)' />\n\
        <img src='"+save+"' class='save' onclick='editTag2(this);' value='Save' />");
                

                var img_scope_top = $("#imageMap").offset().top + $("#imageMap").height() - $(this).find(".tagged_box").height();
                var img_scope_left = $("#imageMap").offset().left + $("#imageMap").width() - $(this).find(".tagged_box").width();

                $(this).draggable({ containment:[$("#imageMap").offset().left,$("#imageMap").offset().top,img_scope_left,img_scope_top]  });

            });

            var addTag = function(){
                var position = $('#mapper').position();


                var pos_x = position.left;
                var pos_y = position.top;
                var pos_width = $('#mapper').width();
                var pos_height = $('#mapper').height();
                var type = $('#form_panel_add #tag_type option:selected').val();

                $('#planetmap').append('<div class="tagged"  style="width:'+pos_width+'px;height:'+
                    pos_height+'px;left:'+pos_x+'px;top:'+pos_y+'px;" ><div class="tagged_box" id="tag'+nb_tags+'" style="width:'+pos_width+'px;height:'+
                    pos_height+'px;display:none;" ></div><div id="tag'+nb_tags+'t" class="tagged_title" style="top:'+(pos_height+5)+'px;display:none;" id="'+$("#title").val()+'" >'+
                    $("#title").val()+'</div><div id="type" style="display:none;">'+type+'</div></div>');
                tags['tag'+nb_tags] = {title:$("#title").val(), x:pos_x, y:pos_y, w:pos_width, h:pos_height, type:type};
                $("#mapper").hide();
                $("#title").val('');
                $("#form_panel_add").hide();
                
                nb_tags = nb_tags + 1;

            };

            var addFace = function(new_title){
                var position = $('#'+current_tag).parent().position();


                var pos_x = position.left;
                var pos_y = position.top;
                var pos_width = $('#'+current_tag).parent().width();
                var pos_height = $('#'+current_tag).parent().height();
                var type = $('#form_panel_add #tag_type option:selected').val();

                $('#planetmap').append('<div class="tagged"  style="width:'+pos_width+'px;height:'+
                    pos_height+'px;left:'+pos_x+'px;top:'+pos_y+'px;" ><div class="tagged_box" id="tag'+nb_tags+'" style="width:'+pos_width+'px;height:'+
                    pos_height+'px;display:none;" ></div><div id="tag'+nb_tags+'t" class="tagged_title" style="top:'+(pos_height+5)+'px;display:none;" id="'+$("#title").val()+'" >'+
                    new_title+'</div><div id="type" style="display:none;">'+type+'</div></div>');
                tags['tag'+nb_tags] = {title:new_title, x:pos_x, y:pos_y, w:pos_width, h:pos_height};
                $("#mapper").hide();
                $("#title").val('');
                $("#form_panel_add").hide();
                
                nb_tags = nb_tags + 1;

            };

            var saveModifications = function(obj){
                $("#mapper").hide();
                var new_title = $("#form_panel_modify").find("#title").val();
                var type = $("#form_panel_modify").find("#tag_type option:selected").val();
                if(isFace){
                    addFace(new_title);
                    deleteFace(null);
                }else{                
                    $("#"+current_tag+"t").text(new_title);
                    tags[current_tag].title = new_title;     
                    console.log($("#"+current_tag+"t").parent());  
                    $("#"+current_tag+"t").parent().find('#type').text(type);
                    tags[current_tag].type = type;               
                }
                $("#form_panel_modify").hide();
                console.log(tags);
            };

            var openDialog = function(){
                $("#form_panel_add").fadeIn("slow");
            };

            var openDialog2 = function(obj){
                var title = "";
                var type = 'face';
                if(!isFace){
                    title = tags[current_tag].title;
                    type = tags[current_tag].type;
                }
                console.log(tags[current_tag]);
                $("#form_panel_modify").find("#title").val(current_title);
                $("#form_panel_modify").find("#tag_type option:selected").removeAttr('selected');
                $("#form_panel_modify").find("#tag_type option[value='"+type+"']").attr('selected','selected');
                console.log($("#form_panel_modify").find("#tag_type"));
                console.log($("#form_panel_modify").find("#tag_type").find("option[value='"+type+"']"));
                $("#form_panel_modify").fadeIn("slow");
            };

            var showTags = function(){
                $(".tagged_box").css("display","block");
                $(".tagged").css("border","2px solid #EEE");
                $(".tagged2").css("border","2px solid #EEE");
                $(".tagged_title").css("display","block");
            };

            var hideTags = function(){
                $(".tagged_box").css("display","none");
                $(".tagged").css("border","none");
                $(".tagged2").css("border","none");
                $(".tagged_title").css("display","none");
            };

            var sendTags = function(){
                // submit_form = '';
                // nb_tags = 0;
                // for(var i = 0; i < tags.length; i++){
                //     if(tag.length != 0){
                //         submit_form = submit_form + '<input type="hidden" name="tag'+nb_tags+'" value="'+tag.title+';'+tag.x+';'+tag.y+';'+tag.w+';'+tag.h+'">'
                //         nb_tags++;
                //     }
                // }
                // submit_form = '<form method="post" action="/imagetagger" target="TheWindow"> <input type="hidden" name="nb_tags" value="'+nb_tags+'">'+submit_form+"</form>";   
                // $(submit_form).submit();
                var form = document.createElement("form");
                form.setAttribute("method", "post");
                form.setAttribute("action", "/imagetagger");
                //form.setAttribute("target", "view");
                nb_tags2 = 0;
                for(var i = 0; i < nb_tags; i++){
                    var tag = tags['tag'+i];
                     if(tag.title != undefined){
                        var hiddenField = document.createElement("input"); 
                        hiddenField.setAttribute("type", "hidden");
                        hiddenField.setAttribute("name", "tag"+i);
                        hiddenField.setAttribute("value", tag.title+';'+tag.x+';'+tag.y+';'+tag.w+';'+tag.h+';'+tag.type);
                        form.appendChild(hiddenField);
                        nb_tags2++;
                    }
                }
                console.log(nb_tags);
                var hiddenField = document.createElement("input"); 
                        hiddenField.setAttribute("type", "hidden");
                        hiddenField.setAttribute("name", "nb_tags");
                        hiddenField.setAttribute("value", nb_tags2);
                        form.appendChild(hiddenField);
                document.body.appendChild(form);

                //window.open('', 'view');

                form.submit();
                
            };

            var editTag2 = function(obj){
                console.log($(obj).parent())
                current_tag = $(obj).parent().attr("id");
                current_title = $(obj).parent().parent().find(".tagged_title").text().replace(/(\r\n|\n|\r|\s)/gm," ");
                console.log(current_title);
                openDialog2(obj);  
                $(obj).parent().parent().draggable( 'disable' );
                $(obj).parent().parent().removeAttr( 'class' );
                if(isFace){
                    $(obj).parent().parent().addClass( 'tagged2' );

                }else{
                    $(obj).parent().parent().addClass( 'tagged' );
                }

                $(obj).parent().parent().css("border","none");
                $(obj).parent().css("display","none");
                $(obj).parent().parent().find(".tagged_title").css("display","none");
                $(obj).parent().html('');   
            }
		
            var editTag = function(obj){

                $(obj).parent().parent().draggable( 'disable' );
                $(obj).parent().parent().removeAttr( 'class' );
                $(obj).parent().parent().addClass( 'tagged' );
                $(obj).parent().parent().css("border","none");
                $(obj).parent().css("display","none");
                $(obj).parent().parent().find(".tagged_title").css("display","none");
                $(obj).parent().html('');

            }

            var deleteTag = function(obj){
                current_tag = $(obj).parent().attr('id');
                tags[current_tag] = {};
                $(obj).parent().parent().remove();
            };

            var deleteFace = function(obj){
                if(obj!=null){
                    current_tag = $(obj).parent().attr('id');
                    $(obj).parent().parent().remove();
                }else{
                    $('#'+current_tag).parent().remove();
                }
                faces[current_tag] = {};
            }