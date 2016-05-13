window.onload = function setDataSource() {
		if (!!window.EventSource) {
			var source = new EventSource("stream.py");

			source.addEventListener("message", function(e) {
				updatePrice(e.data);
				logMessage(e);
			}, false);

			source.addEventListener("open", function(e) {
				logMessage("OPENED");
			}, false);

			source.addEventListener("error", function(e) {
				logMessage("ERROR");
				if (e.readyState == EventSource.CLOSED) {
					logMessage("CLOSED");
				}
			}, false);
		} else {
			document.getElementById("notSupported").style.display = "block";
		}
	}

	function updatePrice(data) {
		var ar = data.split(":");
		var ticket = ar[0];
		var price = ar[1];
		var el = document.getElementById("t_" + ticket);
		var oldPrice = el.innerHTML;
		el.innerHTML = price;
		if (parseFloat(oldPrice) < parseFloat(price)) {
			el.style.backgroundColor = "lightgreen";
		} else {
			el.style.backgroundColor = "tomato";
		}
		window.setTimeout(function clearBackground() {
			el.style.backgroundColor = "white";
		}, 500);
	}

	function logMessage(obj) {
		var el = document.getElementById("log");
		if (typeof obj === "string") {
			el.innerHTML += obj + "<br>";
		} else {
			el.innerHTML += obj.lastEventId + " - " + obj.data + "<br>";
		}
		el.scrollTop += 20;
	}
