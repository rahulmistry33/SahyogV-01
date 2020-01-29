
if('serviceWorker' in navigator){
    navigator.serviceWorker.register("/scripts/sw.js", { scope: '/scripts/' })
    .then((reg) => console.log('service worker registered'),reg)
    .catch((err) => console.log('service worker not registered'),err)
}