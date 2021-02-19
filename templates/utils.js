<script type="text/javascript">
function logout() {
    console.log("jah")
    localStorage.removeItem("authToken");
    window.location.href = "/home";
}
</script>
