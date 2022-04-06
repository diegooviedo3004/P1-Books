let input_books = document.querySelector('#input_books');
let spinner = document.getElementById("spinner");
async function request() {
    document.getElementById('books_container').innerHTML = ""
    spinner.style.display = 'unset';
    const res = await fetch(`/${input_books.value}`);
    const data = await res.json()
    spinner.style.display = 'none';
    console.log(data)
    for(element of data){
        $('#books_container').append(`<div class="col m-2 p-2"><div class="book">${element[0]}<br>${element[1]}<br>${element[2]}<br>${element[3]}</div></div>`)
    }
}
input_books.addEventListener('keyup',() => {
    if(!(input_books.value == "")){
        request()  
    }
})


