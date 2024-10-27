let isProductClicked = false;

$(document).ready(function() {
    $('.dropdown-menu').on('click', '.list-group-item', function() {
        var selectedItem = $(this).find('h5').text();
        var selectedProductId = $(this).data('id');        
        $('#book_id').val(selectedProductId);
        $('.dropdown-toggle').text(selectedItem);
        isProductClicked = true;
    });
});

const discussionDataElement = document.getElementById('my-data');
async function getDiscussion() {
    const discussionUrl = discussionDataElement.getAttribute('data-discussion-url');
    return fetch(discussionUrl).then((res) => res.json());
}
async function getProduct() {
    const productUrl = discussionDataElement.getAttribute('data-product');
    return fetch(productUrl).then((res) => res.json())
}

async function refreshDiscussion() {
    document.getElementById("discussion_container").innerHTML = "";
    const allDiscussion = await getDiscussion();

    let htmlString = `<table class="table table-row-spacing">
                        <tr style="height:50px;">
                            <th scope="col" style="width:400px;">Produk</th>
                            <th scope="col" style="width:100px;">Pengguna</th>
                            <th scope="col" style="width:100px;"></th>
                        </tr>
                        <tbody class="table-group-divider">
    `;

    allDiscussion.forEach((item) => {
        let database_url=discussionDataElement.getAttribute('database-url');
        const rowUrl = database_url.replace('9999', item.pk);
        let deleteButton = '';
        if (item.fields.owned_by_current_user) {
            deleteButton = `<button class="btn btn-primary" style="font-size:12px;height: auto; text-align: center; background-color: #273faa;" onclick="event.stopPropagation(); deleteDiscussion('${item.fields.user}',${item.pk}); return false; ">Delete</button>`;
        }
        console.log(item.fields.owned_by_current_user)
        htmlString += ` <tr class="mb-1 clickable-row " data-id="${item.pk}" data-url="${rowUrl}" style="height:50px;">
                                <td class="overflow-control" style="width:300px;max-width: 285px;">${item.fields.topic}</td>
                                <td class="overflow-control" style="width:300px;max-width: 285px;">${item.fields.product}</td>
                                <td class="overflow-control" style="width:100px;max-width: 100px;">${item.fields.user}</td>
                                <td class="overflow-control" style="width:100px;max-width: 100px;"> 
                                    ${deleteButton}
                                </td>
                        </tr>`
    });
    htmlString +=  `</tbody></table>`
    document.getElementById("discussion_container").innerHTML = htmlString
    document.querySelectorAll('.clickable-row').forEach(row => {
    row.addEventListener('click', () => {
        const url = row.getAttribute('data-url');
        window.location.href = url;
        });
    });
}

function navigateToDiscussion(url) {
    window.location.href = url;
}

refreshDiscussion()

async function showProduct(){
    document.getElementsByClassName("list-group")[0].innerHTML = "";
    const allProduct = await getProduct();
    let stringHTML="";
    allProduct.forEach((item) => {
        stringHTML += `<a href="#" class="list-group-item list-group-item-action" data-id="${item.pk}">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">${item.fields.name}</h5>
                    </div>
                    <small class="text-body-secondary">${item.fields.restaurant}</small>
                    </a>    `
    });
    document.getElementsByClassName("list-group")[0].innerHTML = stringHTML;
}

function addDiscussion() {
    let formData = new FormData(document.querySelector('#form'));
    let isEmptyFieldDetected = false;
    if(isBookClicked == false){
        alert("Pastikan semua terisi, silakan ulangi");
        return false;
    }
    for (let [key, value] of formData.entries()) {
        if (value.trim() === "") {
            isEmptyFieldDetected = true;
            break;
        }
    }

    if (isEmptyFieldDetected) {
        alert("Pastikan semua terisi, silakan ulangi");
        return false;
    }

    fetch(discussionDataElement.getAttribute('create-question'), {
        method: "POST",
        body: new FormData(document.querySelector('#form'))
    }).then(refreshDiscussion)

    document.getElementById("form").reset()
    document.getElementById("dropdown-product").innerText = "Pilih Produk"
    return false
}

document.getElementById("button_add").onclick = addDiscussion

function deleteDiscussion(username,commentId) {
    const url = `/discussion/delete_question/${username}/${commentId}`;
        fetch(url, {
            method: "GET",
        }).then(response => {
            if (response.status === 201) {
                refreshForum();
            } else {
                console.error("Failed to delete comment");
                alert("Ini bukan pertanyaan dari akun Anda, Anda tidak bisa menghapusnya :)"); // Display an alert with an error message
            }
        })
        .catch(error => {
            console.error("Error deleting comment:", error);
            alert("Error deleting comment. Please try again later."); // Display an alert with an error message
        });
        return false
    }