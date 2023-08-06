persisten_volume_claim = """
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: easier-training-claim
spec:
  storageClassName: default
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
"""