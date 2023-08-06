deployment = """
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: easier-training
  name: pod-easier-training
spec:
  replicas: 1
  selector:
    matchLabels:
      app: easier-training
  template:
    metadata:
      labels:
        app: easier-training
  containers:
  - name: easier-training
    image: easierai/easier_training:1.0
    imagePullPolicy: Always
    envFrom:
      - configMapRef:
          name: easier-training
  restartPolicy: Never
"""

deployment_full = """
apiVersion: v1
kind: Job
metadata:
  labels:
    app: easier-training
  name: pod-easier-training
spec:
  replicas: 1
  selector:
    matchLabels:
      app: easier-training
  template:
    metadata:
      labels:
        app: easier-training
  volumes:
    - name: easier-training
      persistentVolumeClaim:
        claimName: easier-training-claim
  containers:
  - name: easier-training
    image: easierai/easier_training:1.0
    imagePullPolicy: Always
    envFrom:
      - configMapRef:
          name: easier-training
    volumeMounts:
      - mountPath: "/train"
        name: easier-training-claim
  restartPolicy: Always
  initContainers:
    - name: easier-training-load-data
      image: easierai/easier_training_load_data:1.0
      imagePullPolicy: Always
      envFrom:
      - configMapRef:
          name: easier-training
      volumeMounts:
        - mountPath: "/train"
          name: easier-training-claim
  # imagePullSecrets:
  # - name: regcred
"""