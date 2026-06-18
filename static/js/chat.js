
document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.querySelector(
                ".chat-input-form"
            );

        if (!form) return;

        const input =
            document.getElementById(
                "message-input"
            );

        const messagesContainer =
            document.querySelector(
                ".messages-container"
            );

        const fileInput =
            document.getElementById(
                "file-upload"
            );

        const filePreview =
            document.getElementById(
                "file-preview"
            );

        const uploadStatus =
            document.getElementById(
                "upload-status"
            );

        // =====================
        // Auto Grow Textarea
        // =====================

        if (input) {

            input.addEventListener(
                "input",
                () => {

                    input.style.height =
                        "auto";

                    input.style.height =
                        input.scrollHeight +
                        "px";
                }
            );
        }

        // =====================
        // File Upload
        // =====================

        if (fileInput) {

            fileInput.addEventListener(
                "change",
                async function () {

                    const file =
                        this.files[0];

                    if (!file) return;

                    filePreview.innerHTML = `
                        <div class="file-card">
                            📄 ${file.name}
                        </div>
                    `;

                    uploadStatus.innerText =
                        "Uploading...";

                    const formData =
                        new FormData();

                    formData.append(
                        "file",
                        file
                    );

                    try {

                        const response =
                            await fetch(
                                "/upload",
                                {
                                    method: "POST",
                                    body: formData
                                }
                            );

                        const data =
                            await response.json();

                        if (data.success) {

                            uploadStatus.innerText =
                                "Ready for analysis";

                        } else {

                            uploadStatus.innerText =
                                data.error ||
                                "Upload failed";
                        }

                    } catch (error) {

                        console.error(
                            error
                        );

                        uploadStatus.innerText =
                            "Upload failed";
                    }
                }
            );
        }

        // =====================
        // Send Message
        // =====================

        form.addEventListener(
            "submit",
            async (e) => {

                e.preventDefault();

                const message =
                    input.value.trim();

                if (!message) return;

                appendUserMessage(
                    message
                );

                input.value = "";

                input.style.height =
                    "auto";

                scrollToBottom();

                const thinking =
                    createThinkingMessage();

                messagesContainer.appendChild(
                    thinking
                );

                scrollToBottom();

                try {

                    const response =
                        await fetch(
                            "/api/chat",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                    "application/json"
                                },

                                body: JSON.stringify({

                                    message:

                                    message,

                                    conversation_id:

                                    form.dataset
                                    .conversationId
                                })
                            }
                        );

                    const data =
                        await response.json();

                    document
                        .getElementById(
                            "thinking-message"
                        )
                        ?.remove();

                        appendAssistantMessage(
                            data.assistant_message.content
                        );

                        scrollToBottom();

                        if (
                            !form.dataset.conversationId
                        ) {

                            window.location.href =
                                "/conversation/" +
                                data.conversation_id;

                        }

                } catch (error) {

                    console.error(
                        error
                    );

                    document
                        .getElementById(
                            "thinking-message"
                        )
                        ?.remove();
                }
            }
        );

        addCopyButtons();

        scrollToBottom();

        // =====================
        // Helpers
        // =====================

        function appendUserMessage(
            message
        ) {

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                "message user";

            div.innerHTML = `
                <div class="message-wrapper user-wrapper">

                    <div class="message-content">

                        ${escapeHtml(
                            message
                        )}

                    </div>

                    <div class="message-actions">

                        <button
                            onclick="copyUserMessage(this)"
                        >
                            📋
                        </button>

                        <button
                            onclick="editUserMessage(this)"
                        >
                            ✏️
                        </button>

                    </div>

                </div>
            `;

            messagesContainer.appendChild(
                div
            );
        }

        function appendAssistantMessage(
            content
        ) {

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                "message assistant";

            div.innerHTML = `
                <div class="message-wrapper assistant-wrapper">

                    <div class="assistant-avatar">
                        AI
                    </div>

                    <div class="assistant-body">

                        <div class="message-content markdown-body">

                            ${content}

                        </div>

                        <div class="assistant-actions">

                            <button
                                onclick="copyAssistantMessage(this)"
                            >
                                📋
                            </button>

                            <button>
                                🔄
                            </button>

                            <button>
                                👍
                            </button>

                            <button>
                                👎
                            </button>

                        </div>

                    </div>

                </div>
            `;

            messagesContainer.appendChild(
                div
            );

            if (window.hljs) {

                div
                    .querySelectorAll(
                        "pre code"
                    )
                    .forEach(
                        block => {

                            hljs.highlightElement(
                                block
                            );
                        }
                    );
            }

            addCopyButtons();
        }

        function createThinkingMessage() {

            const div =
                document.createElement(
                    "div"
                );

            div.id =
                "thinking-message";

            div.className =
                "message assistant";

            div.innerHTML = `
                <div class="message-wrapper assistant-wrapper">

                    <div class="assistant-avatar">
                        AI
                    </div>

                    <div class="assistant-body">

                        <div class="message-content">

                            Thinking...

                        </div>

                    </div>

                </div>
            `;

            return div;
        }

        function scrollToBottom() {

            messagesContainer.scrollTop =
                messagesContainer.scrollHeight;
        }

        function escapeHtml(
            text
        ) {

            const div =
                document.createElement(
                    "div"
                );

            div.textContent =
                text;

            return div.innerHTML;
        }
    }
);

// =====================
// Profile Menu
// =====================

function toggleProfileMenu() {

    document
        .getElementById(
            "profile-menu"
        )
        ?.classList.toggle(
            "show"
        );
}

// =====================
// Copy User Message
// =====================

function copyUserMessage(
    button
) {

    const text =
        button
            .closest(
                ".message-wrapper"
            )
            .querySelector(
                ".message-content"
            )
            .innerText;

    navigator.clipboard
        .writeText(text);

    button.innerText =
        "✅";

    setTimeout(
        () => {

            button.innerText =
                "📋";

        },
        1500
    );
}

// =====================
// Copy AI Message
// =====================

function copyAssistantMessage(
    button
) {

    const text =
        button
            .closest(
                ".assistant-body"
            )
            .querySelector(
                ".message-content"
            )
            .innerText;

    navigator.clipboard
        .writeText(text);

    button.innerText =
        "✅";

    setTimeout(
        () => {

            button.innerText =
                "📋";

        },
        1500
    );
}

// =====================
// Copy Code Blocks
// =====================

function addCopyButtons() {

    document
        .querySelectorAll(
            ".markdown-body pre"
        )
        .forEach(pre => {

            if (
                pre.querySelector(
                    ".copy-code-btn"
                )
            ) return;

            const btn =
                document.createElement(
                    "button"
                );

            btn.className =
                "copy-code-btn";

            btn.innerText =
                "Copy";

            btn.onclick =
                async () => {

                    const code =
                        pre.querySelector(
                            "code"
                        );

                    if (!code) return;

                    await navigator
                        .clipboard
                        .writeText(
                            code.innerText
                        );

                    btn.innerText =
                        "Copied";

                    setTimeout(
                        () => {

                            btn.innerText =
                                "Copy";

                        },
                        2000
                    );
                };

            pre.style.position =
                "relative";

            pre.appendChild(
                btn
            );
        });
}


// =====================
// Edit User Message
// =====================

function editUserMessage(
    button
) {

    const wrapper =
        button.closest(
            ".message-wrapper"
        );

    const messageContent =
        wrapper.querySelector(
            ".message-content"
        );

    const oldText =
        messageContent.innerText;

    messageContent.innerHTML = `

        <textarea
            class="edit-message-box"
        >${oldText}</textarea>

        <div
            class="edit-actions"
        >

            <button
                class="save-edit-btn"
                onclick="
                saveEditedMessage(
                    this
                )"
            >
                Save
            </button>

            <button
                class="cancel-edit-btn"
                onclick="
                cancelEditMessage(
                    this,
                    ${JSON.stringify(oldText)}
                )"
            >
                Cancel
            </button>

        </div>

    `;

    const textarea =
        messageContent.querySelector(
            "textarea"
        );

    textarea.focus();

    textarea.setSelectionRange(
        textarea.value.length,
        textarea.value.length
    );
}


// =====================
// Save Edit
// =====================

async function saveEditedMessage(
    button
) {

    const messageContent =
        button.closest(
            ".message-content"
        );

    const textarea =
        messageContent.querySelector(
            "textarea"
        );

    const newText =
        textarea.value.trim();

    if (!newText) return;

    messageContent.innerHTML =
        escapeHtml(newText);

    // Optional:
    // Automatically place edited
    // text back into input box

    const input =
        document.getElementById(
            "message-input"
        );

    if (input) {

        input.value =
            newText;

        input.focus();
    }
}


// =====================
// Cancel Edit
// =====================

function cancelEditMessage(
    button,
    oldText
) {

    const messageContent =
        button.closest(
            ".message-content"
        );

    messageContent.innerHTML =
        escapeHtml(oldText);
}


// =====================
// Global Escape Helper
// =====================

function escapeHtml(
    text
) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        text;

    return div.innerHTML;
}


function toggleConversationMenu(
    event,
    id
){

    event.preventDefault();

    event.stopPropagation();

    document
        .querySelectorAll(
            ".conversation-menu"
        )
        .forEach(menu=>{

            if(
                menu.id !==
                "conversation-menu-"+id
            ){

                menu.classList.remove(
                    "show"
                );

            }

        });

    document
        .getElementById(
            "conversation-menu-"+id
        )
        .classList.toggle(
            "show"
        );

}

document.addEventListener(
    "click",
    ()=>{

        document
            .querySelectorAll(
                ".conversation-menu"
            )
            .forEach(menu=>{

                menu.classList.remove(
                    "show"
                );

            });

    }
);

