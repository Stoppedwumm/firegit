
# Firegit

Store your code project in firestore


## Installation

Download the latest release

## Usage

Run it with

```bash
release_osx [download|upload]
```
or
```cmd
release_binbows.exe [download|upload]
```

Note that you must have an `ServiceAccountKey.json` file in the code directory. You can obtain one in the firebase project settings under `Service Accounts`
## API Reference

### Download from server
```bash
[executable] download
```

### Upload to server
**WARNING: DELETES ANY FILES FROM THE SERVER THAT AREN'T ON THE CLIENT,** I recommend running Download and then making your changes.
```bash
[executable] upload
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
