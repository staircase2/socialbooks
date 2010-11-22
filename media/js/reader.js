/**
 * The SocialBooks Reader
 *
 **/

var Reader = (typeof(reader) == 'undefined')?{}:reader;

// Define Reader functions

Reader.load = function(bookdata, elem, chapter) {

	this.__book = bookdata;
	this.__current_chapter = 0
	
	// Should we load a chapter?
	if(typeof(chapter) != 'undefined') {
		if(typeof(chapter) == 'number') {
			this.__current_chapter = chapter;
		}
		else if(typeof(chapter) == 'string') {
			this.__current_chapter = (isNaN(parseInt(chapter)))?null:parseInt(chapter);
		}
	}
	else {
		this.__current_chapter = 0;
	}
	
	// Prep the book content to display
	var chapter_elem = $('<div class="chapter"></div>').html(bookdata.getComponent(bookdata.getComponents()[this.__current_chapter]))
	$(elem).html(chapter_elem);

	
	// Set up the Reader to automatically queue the next chapter
	$(elem).scroll(function(){
		if($(elem).scrollTop() + $(elem).height() >= $('#reader .chapter').last().height()) { console.log("Loading new chapter");
			Reader.__current_chapter += 1;
			var next_chapter = $('<div class="chapter"></div>').html(Reader.__book.getComponent(Reader.__book.getComponents()[Reader.__current_chapter]))
			
			$(elem).append(next_chapter)
		}
	})

	// Trigger the first scroll
	$('#reader').trigger('scroll');

}

