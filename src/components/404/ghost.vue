<template>
        <div class="ghost">
            <div class="body">
                <i :class="[{left:left}, {right:right}, {top:top}, {bottom:bottom}]"></i>
            </div>
        </div>
</template>

<script>
export default {
    props: {
        left: {
            type: Boolean,
            default: false
        },
        right: {
            type: Boolean,
            default: false
        },
        top: {
            type: Boolean,
            default: false
        },
        bottom: {
            type: Boolean,
            default: false
        }
  },
}
</script>

<style scoped>
.ghost {
    width: 105px;
    float: right;
}

.ghost::after {
    content: " ";
    display: block;
    height: 15px;
    border-radius: 50%;
    margin-top: 20px;
    background: rgba(0,0,0,.1);
    animation: shadow-fade 3s alternate infinite ease-in-out;
}

.body {
    display: block;
    height: 120px;
    padding-top: 35px;
    background: #fff;
    position: relative;
    border-radius: 70px 70px 0 0;
    text-align: center;
    animation: ghost-float 3s alternate infinite ease-in-out;
}

@keyframes shadow-fade {
    0% {
        background: rgba(0,0,0,.3)
    }

    100% {
        background: rgba(0,0,0,.05)
    }
}

@keyframes ghost-float {
    0% {
        transform: translateY(0);
    }

    100% {
        transform: translateY(-20px);
    }
}

.body::after {
    content: " ";
    display: block;
    width: 100%;
    height: 10px;
    position: absolute;
    bottom: -9px;
    background-position: center top;
    background-repeat: repeat-x;
    background-image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0nMTcnIGhlaWdodD0nMTcnIHhtbG5zPSdodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZycgIHZpZXdCb3g9JzAgMCAxMDAgMTAwJz4KCTxsaW5lYXJHcmFkaWVudCBpZD0nZzEnIHgxPScwJScgeTE9JzAlJyB4Mj0nMTAwJScgeTI9JzAlJz4KCQk8c3RvcCBvZmZzZXQ9JzAlJyBzdHlsZT0nc3RvcC1jb2xvcjojOTk5OTk5O3N0b3Atb3BhY2l0eToxJyAvPgoJCTxzdG9wIG9mZnNldD0nMTAwJScgc3R5bGU9J3N0b3AtY29sb3I6I2ZiZGE1OTtzdG9wLW9wYWNpdHk6MCcgLz4KCTwvbGluZWFyR3JhZGllbnQ+Cgk8bGluZWFyR3JhZGllbnQgaWQ9J2cyJyB4MT0nMCUnIHkxPScwJScgeDI9JzAlJyB5Mj0nMTAwJSc+CgkJPHN0b3Agb2Zmc2V0PScwJScgc3R5bGU9J3N0b3AtY29sb3I6Izk5OTk5OTtzdG9wLW9wYWNpdHk6MScgLz4KCQk8c3RvcCBvZmZzZXQ9JzEwMCUnIHN0eWxlPSdzdG9wLWNvbG9yOiNmYmRhNTk7c3RvcC1vcGFjaXR5OjAnIC8+Cgk8L2xpbmVhckdyYWRpZW50PgoJPHJhZGlhbEdyYWRpZW50IGlkPSdnMycgY3g9JzAlJyBjeT0nMCUnIHI9JzEwMCUnPgoJCTxzdG9wIG9mZnNldD0nMCUnIHN0eWxlPSdzdG9wLWNvbG9yOiM5OTk5OTk7c3RvcC1vcGFjaXR5OjEnIC8+CgkJPHN0b3Agb2Zmc2V0PScxMDAlJyBzdHlsZT0nc3RvcC1jb2xvcjojZmJkYTU5O3N0b3Atb3BhY2l0eTowJyAvPgoJPC9yYWRpYWxHcmFkaWVudD4KCTxnIHRyYW5zZm9ybT0ncm90YXRlKDQ1KSB0cmFuc2xhdGUoMjEuMiAtNDkuNSknPgoJCTxyZWN0IHg9Jy01MCUnIHk9Jy01MCUnIHdpZHRoPScxMDAlJyBoZWlnaHQ9JzEwMCUnIGZpbGw9JyNmZmZmZmYnIC8+CgkJPHJlY3QgeD0nNTAlJyB5PSctNTAlJyB3aWR0aD0nMCUnIGhlaWdodD0nMTAwJScgZmlsbD0ndXJsKCNnMSknIC8+CgkJPHJlY3QgeD0nLTUwJScgeT0nNTAlJyB3aWR0aD0nMTAwJScgaGVpZ2h0PScwJScgZmlsbD0ndXJsKCNnMiknIC8+CgkJPHJlY3QgeD0nNTAlJyB5PSc1MCUnIHdpZHRoPScwJScgaGVpZ2h0PScwJScgZmlsbD0ndXJsKCNnMyknIC8+Cgk8L2c+Cjwvc3ZnPg==);
}

:before ::after {
    box-sizing: border-box;
}


@font-face {
    font-family: icons;
    src: url(../fonts/icons.eot?64c061773912345c985cb3365a710a98);
    src: url(../fonts/icons.eot?#iefix) format("embedded-opentype"),url(../fonts/icons.woff?64c061773912345c985cb3365a710a98) format("woff"),url(../fonts/icons.ttf?64c061773912345c985cb3365a710a98) format("truetype");
    font-weight: 400;
    font-style: normal
}

i {
    display: inline-block;
    vertical-align: middle;
    line-height: 1;
    font-weight: 400;
    font-style: normal;
    speak: none;
    text-decoration: inherit;
    text-transform: none;
    text-rendering: auto;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;

    color: #454e57;
    font-size: 40px;
    animation: ghost-blink 4s infinite ease;
    position: relative;
    transition: all .1s ease;
}

@keyframes ghost-blink {
    0% {
        transform: scale(1,0)
    }

    5% {
        transform: scale(1,1)
    }

    100% {
        transform: scale(1,1)
    }
}

i::before {
    font-family: icons;
    content: "\f107";
}

i.right {
    margin-right: -25px;
}

i.left {
    margin-left: -25px;
}

i.top {
    margin-top: -15px;
}

i.bottom {
    margin-top: 15px;
}
</style>