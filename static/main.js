const imgContainer = document.querySelector('.image-container');

function showFile(input){
	let file = input.files[0];
	imgUrl = URL.createObjectURL(file);
	console.log('url', imgUrl);
	console.log(file);
	imgContainer.innerHTML = '<img src = "'+imgUrl+ '"width="450" height="450" alt = "user-input-image"/>';
}

async function getUserFile(){
	// more at https://fjolt.com/article/javascript-new-file-system-api

    try {
        directory = await window.showDirectoryPicker({
            startIn: 'desktop'
        });

        for await (const entry of directory.values()) {
            let newEl = document.createElement('div');
            newEl.innerHTML = `<strong>${entry.name}</strong> - ${entry.kind}`;
            document.getElementById('folder-info').append(newEl);
        }
    } catch(e) {
        console.log(e);
    }

