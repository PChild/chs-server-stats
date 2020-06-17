let userContainer = document.getElementsByClassName('members-1998pB')[0];
let toScroll = userContainer.clientHeight;

let outData = '';
let memberCount = 0;

let curData = userContainer.getElementsByClassName('member-3-YXUe');

let curMin = 0;
let setMax = parseInt(curData[0].getAttribute('aria-setsize'));
let foundLast = false;
let loops = 25;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}


while (!foundLast && loops >= 0) {
	for (const i in curData) {
		let curVal = parseInt(curData[i].ariaPosInSet);
		
		if (curMin < curVal) {
			outData += curData[i].textContent + '\n';
			memberCount += 1;
		}
		
		if (curVal >= setMax) {
			foundLast = true;
			console.log('Found last!');
			break;
		}
	}
	console.log(memberCount + ' users found so far');
	loops--;
	curMin = parseInt(curData[curData.length - 1].ariaPosInSet);
	userContainer.scrollBy(0, toScroll);
	await sleep(1000);
}

download(outData, 'chsUsers.txt', 'text/plain');