# 🚀 EasyMonitor - Integração MQTT com Home Assistant

[![Latest Release](https://img.shields.io/github/v/release/nilsonpessim/easymonitor-hacs?style=for-the-badge)](https://github.com/nilsonpessim/easymonitor-hacs/releases)
[![License](https://img.shields.io/github/license/nilsonpessim/easymonitor-hacs?style=for-the-badge)](LICENSE)
[![Home Assistant Version](https://img.shields.io/badge/Home%20Assistant-2023.1.0%2B-blue?style=for-the-badge)](https://www.home-assistant.io/)
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
3. Informe o host e credenciais do seu broker MQTT
4. Os dispositivos serão detectados automaticamente conforme se conectarem

---

## 📡 Sensores Suportados

| Identificador  | Nome                | Unidade | Ícone                |
|----------------|---------------------|---------|----------------------|
| `tempCH1`      | Temperatura CH1     | °C      | `mdi:thermometer`    |
| `tempCH2`      | Temperatura CH2     | °C      | `mdi:thermometer`    |
| `humiCH1`      | Umidade CH1         | %       | `mdi:water-percent`  |
| `humiCH2`      | Umidade CH2         | %       | `mdi:water-percent`  |
| `voltageDC0`   | Tensão DC0          | V       | `mdi:flash`          |
| `voltageDC1`   | Tensão DC1          | V       | `mdi:flash`          |
| `voltageAC0`   | Status AC0          | on/off  | `mdi:flash`          |

---

## 🧭 Entidades e Dispositivos

- Cada dispositivo é identificado por um ID único (gerado via MAC Address)
- As entidades são automaticamente criadas **somente para os sensores que estão sendo enviados**
- Os dispositivos ficam organizados na interface do Home Assistant por nome/modelo, com suporte ao botão de ação

---

## 🧩 Botões e Serviços

É possível chamar os serviços manualmente:

```
service: easymonitor.remover_dispositivo
data:
  device_id: EASYM_BA84B
```

```
service: easymonitor.resetar_status
data:
  device_id: EASYM_BA84B
```

---

## 🔄 Automação Sugerida

Você pode criar automações com base nos valores dos sensores.  
Exemplo: enviar notificação se `voltageAC0` ficar como "off".

---

## 🛠️ Solução de Problemas

### Os sensores não aparecem?
- Verifique se o broker MQTT está funcionando
- Certifique-se de que o dispositivo publicou no tópico `/status`
- Reinicie o Home Assistant

### Dispositivos duplicados?
- Pode acontecer se o ID não for fixo
- Use o ID baseado no MAC do dispositivo para garantir unicidade

---

## 🤝 Contribuições

Pull Requests e Issues são bem-vindos!  
👉 GitHub: [github.com/nilsonpessim/easymonitor-hacs](https://github.com/nilsonpessim/easymonitor-hacs)

---

## 💡 Desenvolvido por **TechLabs**  
🔗 [easymonitor.com.br](https://easymonitor.com.br)
