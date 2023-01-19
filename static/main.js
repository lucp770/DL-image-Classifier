const imgContainer = document.querySelector('.image-container');
const contButton = document.querySelector('.continue-button');

let file = undefined;
let errorMessage;
let Model = 'VGG';


function showFile(input){
	file = input.files[0];
	imgUrl = URL.createObjectURL(file);
	imgContainer.innerHTML = '<img class ="img" src = "'+imgUrl+ '" alt = "user-input-image"/>';
}

function userCanProceed(){
    if (!Model){
        errorMessage = 'Please select a Classification Model';
        return false;
    }

    if (file==undefined){
        errorMessage =  'Please select an image from your computer. '
        return false;
    }
    return true;
}

function postData(){

    let userAuth = userCanProceed();

    if (userAuth){
        // get all the image data 
        console.log(file);

        // execute fetch to the server, passing header and body.
        let options = {method: "POST",
        body: file,
        headers: {'content-type':'image/png'}
        }

        let r = fetch('/',options);
        console.log(r);

        r.then(res=>console.log(res));

        // change the
        console.log('post sucessfull')
    }
    else{
        console.log('ERROR');
    }
}

contButton.addEventListener('click',(e)=>{
    e.preventDefault();
    postData();
})
