# 🚀 EasyMonitor - Integração MQTT com Home Assistant

[![Latest Release](https://img.shields.io/github/v/release/nilsonpessim/easymonitor-hacs?style=for-the-badge)](https://github.com/nilsonpessim/easymonitor-hacs/releases)
[![License](https://img.shields.io/github/license/nilsonpessim/easymonitor-hacs?style=for-the-badge)](LICENSE)
[![Home Assistant Version](https://img.shields.io/badge/Home%20Assistant-2025.3.0%2B-blue?style=for-the-badge)](https://www.home-assistant.io/)
[![HACS Custom Integration](https://img.shields.io/badge/HACS-Custom%20Integration-orange?style=for-the-badge)](https://hacs.xyz/)

**EasyMonitor** é uma integração personalizada para o **Home Assistant** que detecta automaticamente dispositivos da linha *EasyMonitor* conectados via **MQTT**, exibindo sensores organizados por dispositivo.

---

## 📌 Recursos

✔ Integração com **MQTT**  
✔ Detecção automática dos dispositivos EasyMonitor  
✔ Criação de **entidades organizadas por dispositivo**  
✔ Suporte a sensores de **temperatura**, **umidade**, **tensão DC** e **status AC**  
✔ Compatível com instalação via **HACS**  

---

## 🔧 Instalação

### ✅ Via HACS

1. Acesse **HACS > Integrações**
2. Clique no menu `⋮` → **Repositórios Personalizados**
3. Adicione: `https://github.com/nilsonpessim/easymonitor-hacs`
4. Selecione a categoria **Integração**
5. Instale e **reinicie o Home Assistant**

### 🛠️ Instalação Manual

1. Copie a pasta `easymonitor` para `config/custom_components/`
2. Reinicie o Home Assistant

---

## ⚙ Configuração

1. Vá em **Configurações > Dispositivos e Serviços**
2. Clique em **Adicionar Integração** → **EasyMonitor**
3. Os dispositivos serão detectados automaticamente conforme se conectarem

---

## 📡 Sensores Suportados

| Identificador  | Nome                | Unidade | Ícone |
|----------------|---------------------|---------|-------|
| `tempCH1`      | Temperatura CH1     | °C      |   🌡️  |
| `tempCH2`      | Temperatura CH2     | °C      |   🌡️  |
| `humiCH1`      | Umidade CH1         | %       |   💧  |
| `humiCH2`      | Umidade CH2         | %       |   💧  |
| `voltageDC0`   | Tensão DC0          | V       |   ⚡  |
| `voltageDC1`   | Tensão DC1          | V       |   ⚡  |
| `voltageAC0`   | Status AC0          | on/off  |   🗼  |

---

## 🧭 Entidades e Dispositivos

- Cada dispositivo é identificado por um ID único (gerado pelo EasyMonitor)
- As entidades são automaticamente criadas **somente para os sensores que estão sendo enviados**
- Os dispositivos ficam organizados na interface do Home Assistant

---

## 🧩 Ações

É possível remover o dispositivo pela integração ou chamar a ação manualmente:

```
action: easymonitor.remover_dispositivo
data:
  device_id: EASYM_BA84B
```

Após remove-lo, recarregue a integração via menu!

---

## 🔄 Automação Sugerida

Você pode criar automações com base nos valores dos sensores (Entidades).  
Exemplo: enviar notificação se `voltageAC0` ficar como "off".

---

## 🛠️ Solução de Problemas

### Os sensores não aparecem?
- Verifique se o broker MQTT está funcionando
- Certifique-se de que o dispositivo publicou no tópico `/status`
- Reinicie o Home Assistant

---

## 🤝 Contribuições

Pull Requests e Issues são bem-vindos!  
👉 GitHub: [github.com/nilsonpessim/easymonitor-hacs](https://github.com/nilsonpessim/easymonitor-hacs)

---

## 💡 Desenvolvido por **Nilson Pessim**  
🔗 [easymonitor.com.br](https://easymonitor.com.br)
