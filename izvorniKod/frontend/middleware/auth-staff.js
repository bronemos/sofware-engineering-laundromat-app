export default async function({$auth, next, store, redirect}) {
    let user = $auth.$state.user;
    if (!(user && (user.is_staff || user.is_superuser))){
        return redirect('/')
    }
}