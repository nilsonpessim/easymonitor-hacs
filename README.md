# 🚀 EasyMonitor - Home Assistant Integration via MQTT  

[![Latest Release](https://img.shields.io/github/v/release/nilsonpessim/easymonitor-hacs?style=for-the-badge)](https://github.com/nilsonpessim/easymonitor-hacs/releases)
[![License](https://img.shields.io/github/license/nilsonpessim/easymonitor-hacs?style=for-the-badge)](LICENSE)
[![Home Assistant Version](https://img.shields.io/badge/Home%20Assistant-2023.1.0%2B-blue?style=for-the-badge)](https://www.home-assistant.io/)
[![HACS Custom Integration](https://img.shields.io/badge/HACS-Custom%20Integration-orange?style=for-the-badge)](https://hacs.xyz/)

EasyMonitor é uma **integração personalizada para o Home Assistant** que permite monitorar sensores e dispositivos conectados via **MQTT**. Com suporte para medições de temperatura, umidade e tensão AC/DC, essa integração facilita o gerenciamento de dispositivos IoT da **TechLabs**.

---

## 📌 **Recursos**
✔ Integração nativa com **MQTT**  
✔ Detecção automática de dispositivos EasyMonitor  
✔ Suporte a múltiplos sensores: **Temperatura, Umidade, Tensão DC e AC**  
✔ Configuração simples via **HACS**  

---

## 🔧 **Instalação**
### **1️⃣ Instalar via HACS**
1. Acesse **HACS**
2. Clique no menu `⋮` (canto superior direito) e selecione **Repositorios Personalizados**  
3. Adicione o repositório:  https://github.com/nilsonpessim/easymonitor-hacs
4. Escolha a categoria **Integração**  
5. Instale e reinicie o Home Assistant  

### **2️⃣ Instalação Manual**
1. No Home Assistant, vá até a pasta de configurações: /config/custom_components/
2. Clone o repositório: git clone https://github.com/nilsonpessim/easymonitor-hacs.git easymonitor
3. Reinicie o Home Assistant

---

## ⚙ **Configuração**
### **Adicionando a Integração**
1. No Home Assistant, vá até **Configurações** → **Dispositivos & Serviços**  
2. Clique em **Adicionar Integração** e pesquise por **EasyMonitor**  
3. Conecte-se ao seu broker MQTT  
4. Aguarde a detecção automática dos dispositivos  

---

## 📡 **Sensores Suportados**
| Identificador | Nome               | Unidade | Ícone                  |
|--------------|--------------------|---------|------------------------|
| tempCH1      | Temperatura CH1    | °C      | `mdi:thermometer`      |
| tempCH2      | Temperatura CH2    | °C      | `mdi:thermometer`      |
| humiCH1      | Umidade CH1        | %       | `mdi:water-percent`    |
| humiCH2      | Umidade CH2        | %       | `mdi:water-percent`    |
| voltageDC0   | Tensão DC0         | V       | `mdi:flash`           |
| voltageDC1   | Tensão DC1         | V       | `mdi:flash`           |
| voltageAC0   | Tensão AC0 (on/off) | -       | `mdi:flash`           |

---

## ❓ Solução de Problemas

### 1️⃣ Os sensores não aparecem?
🔹 Verifique se o broker MQTT está configurado corretamente  
🔹 Reinicie o Home Assistant  

### 2️⃣ Dispositivo duplicado após reiniciar?
🔹 Pode ser necessário remover e reinstalar a integração  
🔹 Certifique-se de que o ID do dispositivo é único  
---

## 🛠️ Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um **Pull Request** ou relatar um problema na aba **Issues**.

📌 **Repositório GitHub:** [EasyMonitor HACS](https://github.com/nilsonpessim/easymonitor-hacs)  
🌐 **Website Oficial:** [easymonitor.com.br](https://easymonitor.com.br)  

---

### 💡 Desenvolvido por **TechLabs** - Soluções em IoT e Automação
