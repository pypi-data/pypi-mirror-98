
#include <algorithm>

#include "PROPOSAL/crossection/PhotoIntegral.h"
#include "PROPOSAL/crossection/PhotoInterpolant.h"
#include "PROPOSAL/crossection/factories/PhotonuclearFactory.h"
#include "PROPOSAL/crossection/parametrization/PhotoQ2Integration.h"
#include "PROPOSAL/crossection/parametrization/PhotoRealPhotonAssumption.h"
#include "PROPOSAL/crossection/parametrization/Photonuclear.h"
#include "PROPOSAL/medium/Medium.h"

#include "PROPOSAL/Logging.h"

using namespace PROPOSAL;

PhotonuclearFactory::PhotonuclearFactory()
    : photo_shadow_map_str_()
    , photo_shadow_map_enum_()
    , photo_real_map_str_()
    , photo_real_map_enum_()
    , photo_q2_map_str_()
    , photo_q2_map_enum_()
    , string_enum_()
    , string_shadow_enum_()
{
    // Register all photonuclear parametrizations in lower case!

    RegisterShadowEffect(
        "shadowduttarenosarcevicseckel", ShadowDuttaRenoSarcevicSeckel, &ShadowDuttaRenoSarcevicSeckel::create);
    RegisterShadowEffect("shadowbutkevichmikhailov", ShadowButkevichMikhailov, &ShadowButkevichMikhailov::create);

    RegisterRealPhoton("photozeus", Zeus, &PhotoZeus::create);
    RegisterRealPhoton("photobezrukovbugaev", BezrukovBugaev, &PhotoBezrukovBugaev::create);
    RegisterRealPhoton("photorhode", Rhode, &PhotoRhode::create);
    RegisterRealPhoton("photokokoulin", Kokoulin, &PhotoKokoulin::create);
    RegisterRealPhoton("none", None, nullptr);

    RegisterQ2("photoabramowiczlevinlevymaor91",
               AbramowiczLevinLevyMaor91,
               std::make_pair(&PhotoAbramowiczLevinLevyMaor91::create,
                              &PhotoQ2Interpolant<PhotoAbramowiczLevinLevyMaor91>::create));
    RegisterQ2("photoabramowiczlevinlevymaor97",
               AbramowiczLevinLevyMaor97,
               std::make_pair(&PhotoAbramowiczLevinLevyMaor97::create,
                              &PhotoQ2Interpolant<PhotoAbramowiczLevinLevyMaor97>::create));
    RegisterQ2("photobutkevichmikhailov",
               ButkevichMikhailov,
               std::make_pair(&PhotoButkevichMikhailov::create, &PhotoQ2Interpolant<PhotoButkevichMikhailov>::create));
    RegisterQ2("photorenosarcevicsu",
               RenoSarcevicSu,
               std::make_pair(&PhotoRenoSarcevicSu::create, &PhotoQ2Interpolant<PhotoRenoSarcevicSu>::create));
    RegisterQ2("photoabtft",
               AbtFT,
               std::make_pair(&PhotoAbtFT::create, &PhotoQ2Interpolant<PhotoAbtFT>::create));
    RegisterQ2("photoblockdurandha",
               BlockDurandHa,
               std::make_pair(&PhotoBlockDurandHa::create, &PhotoQ2Interpolant<PhotoBlockDurandHa>::create));
}

PhotonuclearFactory::~PhotonuclearFactory()
{
    photo_shadow_map_str_.clear();
    photo_shadow_map_enum_.clear();

    photo_real_map_str_.clear();
    photo_real_map_enum_.clear();

    photo_q2_map_str_.clear();
    photo_q2_map_enum_.clear();

    string_enum_.clear();
    string_shadow_enum_.clear();
}

// ------------------------------------------------------------------------- //
void PhotonuclearFactory::RegisterShadowEffect(const std::string& name,
                                               const Shadow& shadow,
                                               RegisterShadowEffectFunction create)
{
    photo_shadow_map_str_[name]    = create;
    photo_shadow_map_enum_[shadow] = create;
    string_shadow_enum_.insert(name, shadow);
}

// ------------------------------------------------------------------------- //
void PhotonuclearFactory::RegisterRealPhoton(const std::string& name, Enum enum_t, RegisterRealPhotonFunction create)
{
    photo_real_map_str_[name]    = create;
    photo_real_map_enum_[enum_t] = create;
    string_enum_.insert(name, enum_t);
}

// ------------------------------------------------------------------------- //
void PhotonuclearFactory::RegisterQ2(const std::string& name,
                                     Enum enum_t,
                                     std::pair<RegisterQ2Function, RegisterQ2FunctionInterpolant> create)
{
    photo_q2_map_str_[name]    = create;
    photo_q2_map_enum_[enum_t] = create;
    string_enum_.insert(name, enum_t);
}

// ------------------------------------------------------------------------- //
ShadowEffect* PhotonuclearFactory::CreateShadowEffect(const std::string& name)
{
    std::string name_lower = name;
    std::transform(name.begin(), name.end(), name_lower.begin(), ::tolower);

    PhotoShadowEffectMapString::const_iterator it = photo_shadow_map_str_.find(name_lower);

    if (it != photo_shadow_map_str_.end())
    {
        return it->second();
    } else
    {
        log_fatal("Photonuclear %s not registered!", name.c_str());
        return NULL; // Just to prevent warnings
    }
}

// ------------------------------------------------------------------------- //
ShadowEffect* PhotonuclearFactory::CreateShadowEffect(const Shadow& shadow)
{
    PhotoShadowEffectMapEnum::const_iterator it = photo_shadow_map_enum_.find(shadow);

    if (it != photo_shadow_map_enum_.end())
    {
        return it->second();
    } else
    {
        log_fatal("Photonuclear %s not registered!", typeid(shadow).name());
        return NULL; // Just to prevent warnings
    }
}

// ------------------------------------------------------------------------- //
CrossSection* PhotonuclearFactory::CreatePhotonuclear(const ParticleDef& particle_def,
                                                      std::shared_ptr<const Medium> medium,
                                                      const EnergyCutSettings& cuts,
                                                      const Definition& def) const
{
    if(def.parametrization == PhotonuclearFactory::Enum::None){
        log_fatal("Can't return Photonuclear Crosssection if parametrization is None");
        return NULL;
    }

    PhotoQ2MapEnum::const_iterator it_q2            = photo_q2_map_enum_.find(def.parametrization);
    PhotoRealPhotonMapEnum::const_iterator it_photo = photo_real_map_enum_.find(def.parametrization);

    if (it_q2 != photo_q2_map_enum_.end())
    {
        ShadowEffect* shadow = Get().CreateShadowEffect(def.shadow);

        PhotoIntegral* photo =
            new PhotoIntegral(*it_q2->second.first(particle_def, medium, cuts, def.multiplier, *shadow));
        delete shadow;
        return photo;
    } else if (it_photo != photo_real_map_enum_.end())
    {
        return new PhotoIntegral(*it_photo->second(particle_def, medium, cuts, def.multiplier, def.hard_component));
    } else
    {
        log_fatal("Photonuclear %s not registered!", typeid(def.parametrization).name());
        return NULL; // Just to prevent warnings
    }
}

// ------------------------------------------------------------------------- //
CrossSection* PhotonuclearFactory::CreatePhotonuclear(const ParticleDef& particle_def,
                                                      std::shared_ptr<const Medium> medium,
                                                      const EnergyCutSettings& cuts,
                                                      const Definition& def,
                                                      InterpolationDef interpolation_def) const
{
    if(def.parametrization == PhotonuclearFactory::Enum::None){
        log_fatal("Can't return Photonuclear Crosssection if parametrization is None");
        return NULL;
    }

    PhotoQ2MapEnum::const_iterator it_q2            = photo_q2_map_enum_.find(def.parametrization);
    PhotoRealPhotonMapEnum::const_iterator it_photo = photo_real_map_enum_.find(def.parametrization);

    if (it_q2 != photo_q2_map_enum_.end())
    {
        ShadowEffect* shadow = Get().CreateShadowEffect(def.shadow);

        PhotoInterpolant* photo = new PhotoInterpolant(
            *it_q2->second.second(particle_def, medium, cuts, def.multiplier, *shadow, interpolation_def),
            interpolation_def);
        delete shadow;
        return photo;
    } else if (it_photo != photo_real_map_enum_.end())
    {
        return new PhotoInterpolant(*it_photo->second(particle_def, medium, cuts, def.multiplier, def.hard_component),
                                    interpolation_def);
    } else
    {
        log_fatal("Photonuclear %s not registered!", typeid(def.parametrization).name());
        return NULL; // Just to prevent warnings
    }
}

// ------------------------------------------------------------------------- //
PhotonuclearFactory::Enum PhotonuclearFactory::GetEnumFromString(const std::string& name)
{
    std::string name_lower = name;
    std::transform(name.begin(), name.end(), name_lower.begin(), ::tolower);

    auto& left = string_enum_.GetLeft();
    auto it = left.find(name_lower);
    if (it != left.end())
    {
        return it->second;
    } else
    {
        log_fatal("Photonuclear %s not registered!", name.c_str());
        return PhotonuclearFactory::Fail; // Just to prevent warnings
    }
}

// ------------------------------------------------------------------------- //
std::string PhotonuclearFactory::GetStringFromEnum(const PhotonuclearFactory::Enum& enum_t)
{
    auto& right = string_enum_.GetRight();
    auto it = right.find(enum_t);
    if (it != right.end())
    {
        return it->second;
    } else
    {
        log_fatal("Photonuclear %s not registered!", typeid(enum_t).name());
        return ""; // Just to prevent warnings
    }
}

// ------------------------------------------------------------------------- //
PhotonuclearFactory::Shadow PhotonuclearFactory::GetShadowEnumFromString(const std::string& name)
{
    std::string name_lower = name;
    std::transform(name.begin(), name.end(), name_lower.begin(), ::tolower);

    auto& left = string_shadow_enum_.GetLeft();
    auto it = left.find(name_lower);
    if (it != left.end())
    {
        return it->second;
    } else
    {
        log_fatal("Photonuclear %s not registered!", name.c_str());
        return PhotonuclearFactory::ShadowNone; // Just to prevent warnings
    }
}

// ------------------------------------------------------------------------- //
std::string PhotonuclearFactory::GetStringFromShadowEnum(const Shadow& shadow)
{
    auto& right = string_shadow_enum_.GetRight();
    auto it = right.find(shadow);
    if (it != right.end())
    {
        return it->second;
    } else
    {
        log_fatal("Photonuclear %s not registered!", typeid(shadow).name());
        return ""; // Just to prevent warnings
    }
}
