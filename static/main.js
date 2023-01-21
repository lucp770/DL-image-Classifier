const imgContainer = document.querySelector('.image-container');
const contButton = document.querySelector('.continue-button');

const models = document.querySelectorAll('.model');
const selectModelBtn = document.querySelector('.select-model');

const slideMenu = document.querySelector('.model-selection');
const arrowLogo = document.querySelector('.fa-solid');

const modelInfo = document.querySelector('.model-information');


let file = undefined;
let errorMessage;
let Model = '';


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
        body: {file:file, model: Model},
        headers: {'content-type':'multipart/form-data'}
        }

        delete options.headers['Content-Type'];

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


function sendData(data){
    const formData = new FormData();

    for(const name in data){
        formData.append(name, data[name]);
    }

    let options = {
    method: "POST",
    body: formData
    }

    let r = fetch('/',options);
    r.then(res=>console.log(res));

}

// event listeners

contButton.addEventListener('click',(e)=>{
    e.preventDefault();
    postData();

})

models.forEach(model=>{
    model.addEventListener('click', ()=>{
        console.log(model.innerText);
        // define the model to be selected
        Model = model.innerText;
        console.log('variable Model value: ', Model);

        modelInfo.innerText = 'The model selected is ' + Model;

       
        // remove the selected class from others and add only on the clicked button.
        models.forEach(modelo=>{
            if(modelo.classList.contains('selected')){
                modelo.classList.remove('selected');
            } 
        })
        
         // change the syle, to indicate the selection.
        model.classList.add('selected');

        })
})

selectModelBtn.addEventListener('click', ()=>{

    // check if is visible
    let classes = slideMenu.classList;
    // console.log(classes.contains('visible'));
    if(classes.contains('hidden')){
        console.log('showMenu');
        classes.remove('hidden');

        // change the logo to up arrow.
        arrowLogo.classList.remove('fa-chevron-down');
        arrowLogo.classList.add('fa-chevron-up')
    }
    else{
        console.log('hide Menu')

        classes.add('hidden');

        // change the logo to up down.
        arrowLogo.classList.remove('fa-chevron-up');
        arrowLogo.classList.add('fa-chevron-down')
    }
})