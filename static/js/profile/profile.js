	function load_js()
	{
		$('select').prettyDropdown();
		var tags = new Bloodhound({
	        datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.tag); },
	        queryTokenizer: Bloodhound.tokenizers.whitespace,
	        local: [
	            { tag: 'dog' },
	            { tag: 'cat' },
	            { tag: 'fish' },
	            { tag: 'catfish' },
	            { tag: 'dogfish' }
	        ]
	    });
	    tags.initialize();
	    var screenConsole = $('#console');
	    var logCallbackDataToConsole = function(added, removed) {
	        screenConsole.append('Tag Data: ' + (this.val() || null) + ', Added: ' + added + ', Removed: ' + removed + '\n');
	    };
	    $('.tag-input').tagInput({
	        allowDuplicates: false,
	        typeahead: true,
	        typeaheadOptions: {
	            highlight: true
	        },
	        typeaheadDatasetOptions: {
	            display: function(d) { return d.tag; },
	            source: tags.ttAdapter()
	        },
	        onTagDataChanged: logCallbackDataToConsole
	    });
	}
	function adjustHeight(el){
	    el.style.height = (el.scrollHeight > el.clientHeight) ? (el.scrollHeight)+"px" : "30px";
	}
	
	function showcandidate(pID)
	{
	    $.ajax({
            typ: 'get',
	        url: '/ajax/candidate',
	        success: function (data) {
	            $("#content").html(data);
	        }
	    });
	}
	function add_recruiter(){
		$.ajax({
            url: '/ajax/get_recruiter',
            type: 'get',
            success: function (data) {
                $("#recruiter_experience").append(data);
        		load_js();
            }
        });
    }
    function set_nav_active(pName)
    {
    	if(pName == "profile"){
    		$("#nav_profile").addClass("nav_active");
    	}
    	else if (pName == "order"){
    		$("#nav_order").addClass("nav_active");
    	}
    	else if (pName == "dashboard"){
    		$("#nav_dashboard").addClass("nav_active");
    	}
    }
    function progress_setpos(pStep)
	{
		if(pStep == "profile"){
			$("#progress_head_profile").removeClass("progress-label-active");
			$("#progress_head_order").removeClass("progress-label-active");
			$("#progress_head_payment").removeClass("progress-label-active");
			$("#progress_head_profile").addClass("progress-label-active");
			$("#progress_oval_order").hide();$("#progress_oval_payment").hide();
			$("#progress_progress").hide();
		}
		else if(pStep=="order"){
			$("#progress_head_profile").removeClass("progress-label-active");
			$("#progress_head_order").removeClass("progress-label-active");
			$("#progress_head_payment").removeClass("progress-label-active");
			$("#progress_head_order").addClass("progress-label-active");
			$("#progress_oval_order").show();$("#progress_oval_payment").hide();
			$("#progress_progress").show();
			$("#progress_progress").addClass("half-width");
			$("#progress_progress").removeClass("full-width");
		}
		else if(pStep =="payment"){
			$("#progress_head_profile").removeClass("progress-label-active");
			$("#progress_head_order").removeClass("progress-label-active");
			$("#progress_head_payment").removeClass("progress-label-active");
			$("#progress_head_payment").addClass("progress-label-active");
			$("#progress_oval_order").show();$("#progress_oval_payment").show();
			$("#progress_progress").show();
			$("#progress_progress").removeClass("half-width");
			$("#progress_progress").addClass("full-width");
		}
	}
	function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
	function set_autocomplete(pID,pFile){
		$.ajax({
		    url: pFile,
		    dataType: "text",
		    success: function(data) {
		    	var autoCompleteData = data.split('\n');
		    	$( "#"+pID ).autocomplete({
			        minLength: 0,
			        source: function( request, response ) {
			          var results = $.ui.autocomplete.filter(autoCompleteData, request.term);
			          response(results.slice(0, 10));
			        },
			        focus: function() {
			          return false;
			        },
			        select: function( event, ui ) {
			          var terms = split( this.value );
			          // remove the current input
			          terms.pop();
			          // add the selected item
			          terms.push( ui.item.value );
			          // add placeholder to get the comma-and-space at the end
			          terms.push( "" );
			          this.value = terms.join( "" );
			          return false;
			        }
		        });
		   	}
		});
	}
	function set_search_tag_editor(pID,pTempID,pPlaceholder,pFile,pParent='NULL',pEdit = 'False',pCss = '')
	{
		$.ajax({
		    url: pFile,
		    dataType: "text",
		    success: function(data) {
		    	var autoCompleteData = data.split('\n');
		    	$(pID).tagEditor({
					autocomplete: {
				        delay: 0, // show suggestions immediately
				        position: { collision: 'flip' }, // automatic menu position up/down
				        source: function(request, response) {
			                var results = $.ui.autocomplete.filter(autoCompleteData, request.term);
			                response(results.slice(0, 10)); // Display the first 10 results
		            	}
				    },
		    		forceLowercase: false,
				    placeholder: pPlaceholder,
				    onChange: function(field, editor, tags) {
				       $(pTempID).val(tags.length ? tags.join(', ') : '----');
				    },
				});
				if (pCss != ""){
					$( pParent ).find($(".tag-editor")).attr("style",pCss);
				}
		    }
		});
	}
	function set_tag_editor(pID,pTempID,pPlaceholder,pFile,pParent='NULL',pEdit = 'False',pCss = '')
	{
		$.ajax({
		    url: pFile,
		    dataType: "text",
		    success: function(data) {
		    	var autoCompleteData = data.split('\n');
		    	$(pID).tagEditor({
					autocomplete: {
				        delay: 0, // show suggestions immediately
				        position: { collision: 'flip' }, // automatic menu position up/down
				        source: function(request, response) {
			                var results = $.ui.autocomplete.filter(autoCompleteData, request.term);
			                response(results.slice(0, 10)); // Display the first 10 results
		            	}
				    },
		    		forceLowercase: false,
				    placeholder: pPlaceholder,
				    onChange: function(field, editor, tags) {
				       $(pTempID).val(tags.length ? tags.join(', ') : '----');
				    },
				});
				if (pCss != ""){
					$( pParent ).find($(".tag-editor")).addClass(pCss);
				}
				if(pEdit == 'True' && pParent!="NULL"){
					$( pParent ).find($(".tag-editor")).addClass("border-none");
					var item1 = $( ".tag-editor-delete" );
					$( pParent ).find( item1 ).hide();
					//$(".tag-editor-delete").hide();
					$( pParent ).find($(".tag-editor-tag")).addClass("right-border");
					$( pParent ).find($(".tag-editor-tag")).css("padding-right","10px");
				}
				else if(pEdit=='False' && pParent!="NULL"){
					$( pParent ).find($(".tag-editor")).removeClass("border-none");
					var item1 = $( ".tag-editor-delete" );
					$( pParent ).find( item1 ).show();
					$( pParent ).find($(".tag-editor-tag")).removeClass("right-border");
					$( pParent ).find($(".tag-editor-tag")).css("padding-right","10px");
				}
				return true;
		    }
		});
	}
	function loadaccordion(){
		$(function() {
			var Accordion = function(el, multiple) {
				this.el = el || {};
				this.multiple = multiple || false;

				// Variables privadas
				var links = this.el.find('.link');
				// Evento
				links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
			}

			Accordion.prototype.dropdown = function(e) {
				var $el = e.data.el;
					$this = $(this),
					$next = $this.next();

				$next.slideToggle();
				$this.parent().toggleClass('open');

				if (!e.data.multiple) {
					$el.find('.submenu').not($next).slideUp().parent().removeClass('open');
				};
			}	

			var accordion = new Accordion($('#accordion'), false);
		});
	}
$(document).ready(function() {
	$('form').submit(function () {
	  if ($(document.activeElement).attr('type') == 'submit')
	     return true;
	  else return false;
	});
	load_js();
	var _gaq = _gaq || [];
	_gaq.push(['_setAccount', 'UA-36251023-1']);
	_gaq.push(['_setDomainName', 'jqueryscript.net']);
	_gaq.push(['_trackPageview']);

	(function() {
	var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
	ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
	})();

});


