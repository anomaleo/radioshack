import board
import time

HTML_TEMPLATE = """
<!DOCTYPE html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>Soft Cars</title>
    <style>
        body {
            font-family: Courier, monospace; 
            background:HotPink;
            text-align: center;
            color:Snow;
        }
        input[type="button"] {
            font-family: Courier, monospace;
            background-color:MistyRose; 
            color:Orchid;
            font-size: 48px;
            height: 80px;
            margin: 10px;
            border: 3px solid black;
            border-radius: 20px;
        }
    </style>
    </head>
    <body>
        
        <h1>Soft Cars Remote Control</h1>
    	<input id="fwd" type="button" value="Forward">
        <input id="l" type="button" value="Left">
    	<input id="r" type="button" value="Right">
    	<input id="bwd" type="button" value="Backward">
    	<input id="stop" type="button" value="Stop">
    	<input id="honk" type="button" value="Honk">
    	<input id="flash" type="button" value="Flash">
        
        <p>CPU temperature: <strong>-</strong>&deg;C</p>
        <p>NeoPixel Color: <input type="color"></p>

        <script>
            const cpuTemp = document.querySelector('strong');
            const colorPicker = document.querySelector('input[type="color"]');
            

			let fwd = document.querySelector('input[id="fwd"]');
			fwd.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'forward': 1 } ))
  				ws.send(JSON.stringify( { 'forward': 1 } ));
			}, false);
			
			let bwd = document.querySelector('input[id="bwd"]');
			bwd.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'backward': 1 } ))
  				ws.send(JSON.stringify( { 'backward': 1 } ));
			}, false);

			let l = document.querySelector('input[id="l"]');
			l.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'left': 1 } ))
  				ws.send(JSON.stringify( { 'left': 1 } ));
			}, false);

            let r = document.querySelector('input[id="r"]');
			r.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'right': 1 } ))
  				ws.send(JSON.stringify( { 'right': 1 } ));
			}, false);

            let stop = document.querySelector('input[id="stop"]');
			stop.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'stop': 1 } ))
  				ws.send(JSON.stringify( { 'stop': 1 } ));
			}, false);

            let honk = document.querySelector('input[id="honk"]');
			honk.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'honk': 1 } ))
  				ws.send(JSON.stringify( { 'honk': 1 } ));
			}, false);

            let flash = document.querySelector('input[id="flash"]');
			honk.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'flash': 1 } ))
  				ws.send(JSON.stringify( { 'flash': 1 } ));
			}, false);
            
            let ws = new WebSocket('ws://' + location.host + '/connect-websocket');

            ws.onopen = () => console.log('WebSocket connection opened');
            ws.onclose = () => console.log('WebSocket connection closed');
            ws.onmessage = event => cpuTemp.textContent = event.data;
            ws.onerror = error => cpuTemp.textContent = error;

            colorPicker.oninput = debounce(() => ws.send(colorPicker.value), 200);

            function debounce(callback, delay = 1000) {
                let timeout
                return (...args) => {
                    clearTimeout(timeout)
                    timeout = setTimeout(() => {
                    callback(...args)
                  }, delay)
                }
            }
        </script>
    </body>
</html>
"""