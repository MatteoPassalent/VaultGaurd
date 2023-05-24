
function deleteAccount(accountId) {
    fetch("/delete-account", {
        method: "POST",
        body: JSON.stringify({ accountId: accountId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

async function confirmDelete(accountId) {
    const result = await Swal.fire({
        title: "Are you sure?",
        text: "You will not be able to recover this account information!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
    });

    if (result.isConfirmed) {
        deleteAccount(accountId);
    }
}

function copyToClipboard(elementId) {
    const el = document.getElementById(elementId);
    const text = el.tagName === "INPUT" ? el.value : el.innerText;
    navigator.clipboard.writeText(text)
}


function scrollToBottom() {
    const accountDiv = document.getElementById("account");
    accountDiv.addEventListener("transitionend", () => {
      accountDiv.scrollIntoView({ behavior: "smooth", block: "end" });
    }, { once: true });
  }
  