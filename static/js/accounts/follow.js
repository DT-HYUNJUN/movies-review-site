const form = document.querySelector('#follow-form')
const csrftokenFollow = document.querySelector('[name=csrfmiddlewaretoken]').value;

const followerList = document.querySelector('#follower-list')
const child = followerList.querySelectorAll('div')

const addFollower = (e) => {
  const myName = e.target.dataset.username
  const myNickname = e.target.dataset.myname
  const image = e.target.dataset.image

  const follower = document.createElement('div')
  follower.setAttribute('id', `${myName}`)
  follower.classList.add('m-2')

  const aTag = document.createElement('a')
  aTag.setAttribute('href', `/accounts/profile/${myName}`)
  aTag.classList.add('userinfo-txt')

  const divTag = document.createElement('div')
  divTag.classList.add('userinfo_box')
  
  const img = document.createElement('img')
  img.classList.add('userinfo_img')
  img.setAttribute('src', `${image}`)

  const pTag = document.createElement('p')
  pTag.textContent = myNickname
  pTag.classList.add('text-center')

  divTag.appendChild(img)

  aTag.appendChild(divTag)
  aTag.appendChild(pTag)

  follower.appendChild(aTag)

  followerList.appendChild(follower)
}

const deleteFollower = (e) => {
  const myname = e.target.dataset.username
  const follower = document.querySelector(`#${myname}`)
  followerList.removeChild(follower)
}

const removeNo = () => {
  if (child.length === 0) {
    const noFollowers = followerList.querySelector('p')
    followerList.removeChild(noFollowers)
  }
}

const addNo = () => {
  if (child.length === 0) {
    const addNoFollowers = document.createElement('p')
    addNoFollowers.textContent = 'Follower가 없습니다.'
    followerList.appendChild(addNoFollowers)
  }
}

const formEvent = (e) => {
  e.preventDefault()
  const userPk = e.target.dataset.userpk
  console.log(userPk)
  axios({
    method: 'post',
    url: `/accounts/${userPk}/follow/`,
    headers: {'X-CSRFToken': csrftokenFollow},
  })
    .then((response) => {
      const isFollowed = response.data.is_followed
      const followBtn = document.querySelector('#follow-form > button[type=submit]')

      if (isFollowed === true) {
        const i = followBtn.querySelector('i')
        i.classList.remove('bi', 'bi-person-plus')
        i.classList.add('bi', 'bi-person-dash')
        removeNo()
        addFollower(e)
      } else {
        const i = followBtn.querySelector('i')
        i.classList.remove('bi', 'bi-person-dash')
        i.classList.add('bi', 'bi-person-plus')
        deleteFollower(e)
        addNo()
      }

      const followingsCountTag = document.querySelector('#followings-count')
      const followersCountTag = document.querySelector('#followers-count')
      const followingsCountTagData = response.data.followings_count
      const followersCountTagData = response.data.followers_count
      followingsCountTag.textContent = followingsCountTagData
      followersCountTag.textContent = followersCountTagData
    })
}
form.addEventListener('submit', formEvent)