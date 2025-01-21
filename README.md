
# Firegit

Store your code project in firestore


## Installation

Clone the repo

```bash
git clone https://github.com/Stoppedwumm/firegit.git
```

## Usage

Run it with

```bash
python3 firegit [download|upload]
```

Note that you must have an `ServiceAccountKey.json` file in the code directory. You can obtain one in the firebase project settings under `Service Accounts`
## API Reference

### Download from server
```bash
python3 firegit download
```

### Upload to server
**WARNING: DELETES ANY FILES FROM THE SERVER THAT AREN'T ON THE CLIENT,** I recommend running Download and then making your changes.
```bash
python3 firegit upload
```


## Documentation (module Usage)

### syncFromFirestore
```py
syncFromFirestore()
```
Downloads from server

### syncToFirestore
```py
syncToFirestore(skipDeletion: bool = False)
```
Upload files to server.

#### Args
| ArgName      | Explanation                                                      | Expects | Default |
|--------------|------------------------------------------------------------------|---------|---------|
| skipDeletion | Skip the deletion of server files that don't exist on the client | bool    | False   |
