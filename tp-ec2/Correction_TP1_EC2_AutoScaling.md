# CORRIGÉ FORMATEUR — TP 1  
## Infrastructure scalable avec Amazon EC2, ALB et Auto Scaling Group

---

## 🎯 Objectif du corrigé

Ce document est la **correction complète formateur** du **TP 1**.  
Il décrit **pas à pas** l’architecture attendue, les choix techniques,  
les paramètres importants et les **messages pédagogiques clés** à transmettre.

---

## 🧱 Architecture finale validée

```
Internet
   ↓
Application Load Balancer (ALB)
   ↓
Target Group
   ↓
Auto Scaling Group
   ↓
EC2 instances (multi-AZ)
```

---

## 🪜 Étape 1 — Réseau (VPC)

### Solution attendue
- Utilisation du **VPC par défaut**
- Minimum **2 sous-réseaux publics** dans des AZ différentes
- Internet Gateway déjà attachée

👉 **Point pédagogique**  
Le VPC par défaut est suffisant pour ce TP.  
L’objectif n’est pas le réseau, mais **la scalabilité compute**.

---

## 🪜 Étape 2 — Security Groups

### Security Group ALB
- Entrant :
  - HTTP (80) depuis `0.0.0.0/0`
- Sortant :
  - Tout autorisé

### Security Group EC2
- Entrant :
  - HTTP (80) **uniquement depuis le SG de l’ALB**
- Sortant :
  - Tout autorisé

👉 **Point pédagogique clé**  
Les instances EC2 **ne sont pas exposées à Internet**.

---

## 🪜 Étape 3 — Launch Template

### Paramètres attendus
- AMI : Amazon Linux 2
- Instance type : `t2.micro` ou `t3.micro`
- Key pair : optionnel
- Security Group : EC2 SG
- IAM Role : *aucun requis ici*

### User Data (obligatoire)

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "Hello from $(hostname)" > /var/www/html/index.html
```

👉 **Point pédagogique**  
Le User Data permet d’avoir des instances **stateless** et reproductibles.

---

## 🪜 Étape 4 — Target Group

### Paramètres
- Type : Instance
- Protocol : HTTP
- Port : 80
- Health Check :
  - Path : `/`
  - Healthy threshold : 2
  - Unhealthy threshold : 2

👉 **Point pédagogique**  
Les health checks pilotent :
- le trafic ALB
- les décisions de l’ASG

---

## 🪜 Étape 5 — Application Load Balancer

### Paramètres
- Type : Application Load Balancer
- Scheme : Internet-facing
- Subnets : 2 AZ minimum
- Security Group : ALB SG

### Listener
- HTTP : 80
- Forward vers le Target Group

---

## 🪜 Étape 6 — Auto Scaling Group

### Paramètres attendus
- Launch Template : celui créé
- Subnets : mêmes que l’ALB
- Target Group : associé
- Health check type : ELB

### Capacité
| Type | Valeur |
|---|---|
| Min | 1 |
| Desired | 1 |
| Max | 4 |

👉 **Point pédagogique clé**  
Le Desired Capacity est **un objectif**, pas une garantie.

---

## 🪜 Étape 7 — Scaling Policy

### Policy recommandée
- Type : Target Tracking
- Metric : Average CPU Utilization
- Target value : **50 %**
- Instance warm-up : 300 s

👉 **Pourquoi le scale-in est lent ?**
- Cooldown
- Protection contre le flapping
- Bonne pratique AWS

---

## 🪜 Étape 8 — Tests de charge

### Accès ALB
```
http://<ALB_DNS>
```

### Test de charge (exemple)

```bash
ab -n 100000 -c 200 http://<ALB_DNS>/
```

### Résultat attendu
- CPU ↑
- Scale-out après quelques minutes
- 2 → 3 → 4 instances possibles
- Réponses différentes (`hostname`)

👉 **Point pédagogique**  
Le scaling **n’est jamais instantané**.

---

## 📊 Étape 9 — Observations CloudWatch

### À observer
- EC2 :
  - CPUUtilization
- Auto Scaling :
  - GroupDesiredCapacity
  - GroupInServiceInstances
- ALB :
  - RequestCount
  - TargetResponseTime

---

## 🪜 Étape 10 — Scale-in

### Comportement attendu
- Baisse de charge
- CPU < seuil
- Délai de cooldown
- Suppression progressive des instances

👉 **Question classique stagiaire**  
« Où règle-t-on le temps avant suppression ? »

➡️ **Réponse**  
- Cooldown ASG
- Instance warm-up
- Health checks

---

## 🧹 Nettoyage (obligatoire)

Ordre recommandé :
1. Supprimer l’Auto Scaling Group
2. Supprimer l’ALB
3. Supprimer le Target Group
4. Supprimer le Launch Template
5. Vérifier EC2
