/**
  * Persistence JS Library for SquareCrumbs
  * 
  * Persisting a value saves both to the browser's localStorage and to the server.
  * Retrieving a value goes first to the server, failing which, checks local storage.
  *
  * Values that could not be saved to the server are marked in localStorage, and synced
  * with the server the next time connection is established.
  *
  **/

// Set up the namespaces  
Sq = (typeof(Sq) == 'undefined')?{}:Sq;
Sq.Persist = (typeof(Sq.Persist) == 'undefined')?{}:Sq.Persist;

sqp = Sq.Persist; // Set up a shortcut


// Saves to local storage
sqp.save = function(key, data) {
	if(window.localStorage) { // Do we have local storage capabilities?
		var d = [];
		if(typeof(data) == 'object') { // Are we dealing with an object?

			return localStorage[key] = JSON.stringify(data);

			/*
			for(var i in data) {
							if(/string|number|boolean/.test(typeof(data[i]))) { // Only if typeof(data[i]) is 'string', 'number', or 'boolean'
								d.push(i + "=" + data[i]); 
							}
						}
						return localStorage[key] = d.join(";"); // Concat the data values, and store them
			*/
		}
		else if(/string|number|boolean/.test(typeof(data))) {
			return localStorage[key] = data;
		}	
	}
	else {
		return false
	}
}

// Retrieves from local storage
sqp.get = function(key) {

	if(window.localStorage) {
		var res = localStorage[key]; // Will return null if key is non-existent in localStorage
		if(res) {
			try{
				return JSON.parse(res)
			}
			catch (err){
				return res; // Probably a flat string instead of a JSON string
			}
			/*
			var out = {};
			var r = res.split(";"); // Split the value into its separate parts
			for(var s in r) {
				var val = r[s].split('=');
				console.log(val[0] + " " + val[1])
				out[val[0]] = val[1];
			}
			console.log(out)
			return out; // Returns a hash of key-value pairs. We leave coercion to the caller to handle
			*/
		}
		else {
			return res;
		}
	}
	else {
		return null;
	}
}

// Sends an AJAX request
sqp.send = function(url, data, options) {
	
	// Catch defaults
	options = options || {}
	url = url || null;
	data = data || null;
	onsuccess = options['onsuccess'] || null;
	onerror = options['onerror'] || null;
	oncomplete = options['oncomplete'] || null;
	context = options['context'] || null;
	method = options['method'] || 'post';

	// If we're missing any of our critical arguments, fail immediately
	if(!url) { return false; }
	
	// Let's just assume the presence of jQuery
	if(jQuery) {
		$.ajax({
			url: url,
			type: method,
			data: data,
			success: function(data, textStatus, xhr) {
				if(onsuccess) { console.log("Persist success");
					onsuccess.call(context || this, data, textStatus, xhr);	
				}
			},
			error: function(xhr, textStatus, error) {
				if(onerror) { console.log("Persist error");
					onerror.call(context || this, xhr, textStatus, error);
				}
			},
			complete: function(xhr, textStatus) {
				if(oncomplete){ console.log("Persist complete");
					oncomplete.call(context || this, xhr, textStatus);
				}
			}	
		})	
	}
}



/** BOOKMARKS **/ 
/**
 * SquareCrumbs Bookmarks Persistence Methods 
 *
 **/

Sq.Persist.Bookmarks = (typeof(Sq.Persist.Bookmarks) == 'undefined')?{}:Sq.Persist.Bookmarks;

sqpb = Sq.Persist.Bookmarks; // A shortcut!

sqpb.pendingSync = {'current': null, 'others':[]};

// Saves current reading place
sqpb.save = function(prefix, bookid, component, percent, current) {
	Sq.Persist.save(prefix, {'component': component, 'percent': percent}); // Save to local storage
	Sq.Persist.Bookmarks.saveBookmark(bookid, component, percent, true);
}

// Retrieves current reading place for book
sqpb.get = function(key) {
	return Sq.Persist.get(key);
}

// Save a Bookmark to the server
sqpb.saveBookmark = function(bookid, component, percent, current, options) {
	
	// Fail quickly if we don't have the necessary parameters	
	if(!component || !percent) { return false; }
	
	// Catch defaults
	current = (typeof(current) == 'boolean')?current:false;
	options = options || {};
	
	url = (current)?"/bookmark/current/":"/bookmark/";
	data = {"component": component, "percent": percent, "bookid": bookid};
	
	if(!options.onerror) { // Set error handler only if none exist. We assume it was set for a good reason
		options.onerror = function() { // Update the pendingSync hash in the event that saving to the server failed
			var newbookmark = {'component': component, 'percent': percent};
			if(current){
				Sq.Persist.Bookmarks.pendingSync['current'] = newbookmark;
			}
			else {
				Sq.Persist.Bookmarks.pendingSync['others'].push(newbookmark);
			}
		}
	}
	
	sqp.send(url, data, options);
}


// Get a Bookmark from the server
sqpb.getBookmark = function(bookid, options) {
	
	options = options || {};
	
	// Fail quickly if we don't have the necessary parameters
	if(!bookid) { return false; }
	
	options['method'] = 'get'; // Enforce that we use GET instead of the default POST	
	url = "/bookmark/current/" + bookid + "/";
	
	sqp.send(url, {}, options);
}




