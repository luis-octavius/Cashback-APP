function resolveApiBaseUrl() {
  const configuredBase = window.__APP_CONFIG__?.API_BASE_URL;
  if (configuredBase) {
    return configuredBase.replace(/\/$/, "");
  }

  const isLocalHost = ["localhost", "127.0.0.1", "0.0.0.0"].includes(window.location.hostname);
  return isLocalHost ? "http://127.0.0.1:8000/api/v1/cashback" : "/api/v1/cashback";
}

const API_BASE = resolveApiBaseUrl();

const form = document.getElementById("cashback-form");
const resultNode = document.getElementById("result");
const errorNode = document.getElementById("error");
const historyBody = document.getElementById("history-body");
const historyIpNode = document.getElementById("history-ip");
const refreshBtn = document.getElementById("refresh-history");

function money(value) {
  return Number(value).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function percent(value) {
  return `${Number(value).toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`;
}

function clearMessages() {
  resultNode.textContent = "";
  errorNode.textContent = "";
}

function renderHistory(items) {
  if (!items.length) {
    historyBody.innerHTML = '<tr><td colspan="6">Nenhuma consulta registrada para este IP.</td></tr>';
    return;
  }

  historyBody.innerHTML = items
    .map((item) => {
      const date = new Date(item.created_at);
      return `
        <tr>
          <td>${date.toLocaleString("pt-BR")}</td>
          <td>${item.customer_type.toUpperCase()}</td>
          <td>${money(item.purchase_amount)}</td>
          <td>${percent(item.discount_percent)}</td>
          <td>${money(item.final_amount)}</td>
          <td>${money(item.cashback_amount)}</td>
        </tr>
      `;
    })
    .join("");
}

async function fetchHistory() {
  const response = await fetch(`${API_BASE}/history`);

  if (!response.ok) {
    throw new Error("Falha ao carregar o historico.");
  }

  const data = await response.json();
  historyIpNode.textContent = `IP identificado: ${data.ip_address}`;
  renderHistory(data.items);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessages();

  const payload = {
    customer_type: document.getElementById("customer_type").value,
    purchase_amount: document.getElementById("purchase_amount").value,
    discount_percent: document.getElementById("discount_percent").value,
  };

  try {
    const response = await fetch(`${API_BASE}/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const body = await response.json();
      const msg = body?.detail ? JSON.stringify(body.detail) : "Erro ao calcular cashback.";
      throw new Error(msg);
    }

    const data = await response.json();

    resultNode.textContent = `Cashback calculado: ${money(data.cashback_amount)} (valor final da compra: ${money(
      data.final_amount
    )})`;

    await fetchHistory();
  } catch (error) {
    errorNode.textContent = error.message;
  }
});

refreshBtn.addEventListener("click", async () => {
  clearMessages();
  try {
    await fetchHistory();
  } catch (error) {
    errorNode.textContent = error.message;
  }
});

(async function init() {
  try {
    await fetchHistory();
  } catch (error) {
    errorNode.textContent = error.message;
  }
})();
