service = """
apiVersion: v1
kind: Service
metadata:
  name: service-easier-training
  labels:
    app: easier-training
spec:
  type: NodePort
  # type: LoadBalancer
  ports:
  - name: "5100"
    port: 5100
    targetPort: 5100
  selector:
    app: easier-training
"""