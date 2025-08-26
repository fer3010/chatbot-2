function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const userText = input.value.trim();

  if (userText === "") return;

  // Mostrar mensaje del usuario
  chatBox.innerHTML += `<div><strong>Tú:</strong> ${userText}</div>`;

  // Enviar al backend Flask
  fetch("/get", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ msg: userText })
  })
  .then(response => response.json())
  .then(data => {
    const botReply = data.reply || data.error || "Error en la respuesta";
    chatBox.innerHTML += `<div><strong>Bot:</strong> ${botReply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
  });

  input.value = "";
}
