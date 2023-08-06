ingress = """
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: ingress-easier-training
  kubernetes.io/ingress.allow-http: "true"
  nginx.ingress.kubernetes.io/backend-protocol: HTTP
  nginx.ingress.kubernetes.io/secure-backends: "false"
  labels:
    app: easier-training
spec:
  tls:
  - secretName: wildcard-easier-ai.eu
  rules:
  - host: easier-ai.eu
    http:
      paths:
      - backend:
          serviceName: service-easier-training
          servicePort: 5100
"""