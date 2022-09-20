function Select(){
    let t = document.getElementsByClassName("show");
    if(t.length > 0) t[0].className = "hide";

    let v = document.getElementById("sel").value;
    document.getElementById(v).className = "show";

    document.getElementById("showimg").src = "";
    document.getElementById("find_error").innerHTML = ""
    document.getElementById("result").src = "";
}


function Choose_a_Maze(){
    let file = document.getElementById("inp").files;
    if(file.length > 0){
        let fileReader = new FileReader();

        fileReader.onload = function(event){
            
            document.getElementById("showimg").src = event.target.result;
            document.getElementById("result").src = "";
            document.getElementById("find_error").innerHTML = ""
        };

        fileReader.readAsDataURL(file[0]);
    }
}

function Confirm_the_Maze(){
    let img = document.getElementById("inp").files[0];

    let filereader = new FileReader();
    filereader.onload = function(event){
        //filebase64 = toString(event.target.result);
        eel.return_image(event.target.result)()
    }
    filereader.readAsDataURL(img);
    
}

//for python
eel.expose(setImage)    
function setImage(base64){
    document.getElementById("find_error").innerHTML = "Solved!"
    document.getElementById("result").src = "data:image/png;base64," + base64;
    
}

async function Random_Maze(){
    let r = document.getElementById("row").value;
    let c = document.getElementById("col").value;

    r = Number(r);
    c = Number(c);

    if(r > 40) r = 40;
    if(c > 40) c = 40;
    if(r < 4) r = 4;
    if(c < 4) c = 4;

    let base64 = await eel.Build_maze_by_random(r,c)();
    document.getElementById("showimg").src = "data:image/png;base64," + base64;

}


//照片比例不符合尺寸
eel.expose(Find_error)
function Find_error(){
    document.getElementById("result").src = "";
    document.getElementById("find_error").innerHTML = "I can't recognize this image!"
}
