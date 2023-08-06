apiVersion: v1
kind: PersistentVolume
metadata:
  name: easier-training
  labels:
    type: local
spec:
  storageClassName: default
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/train"